# views.py
import os
import pandas as pd
import json
import threading
import time
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
from src import ObelixProfiler

# Task storage directory
TASK_STORAGE_DIR = os.path.join(settings.MEDIA_ROOT, 'tasks')
os.makedirs(TASK_STORAGE_DIR, exist_ok=True)

def save_task_status(task_id, status, data=None):
    """Save task status to file"""
    task_file = os.path.join(TASK_STORAGE_DIR, f"{task_id}.json")
    task_data = {
        'status': status,
        'timestamp': time.time(),
        'data': data or {}
    }
    with open(task_file, 'w') as f:
        json.dump(task_data, f)

def get_task_status(task_id):
    """Get task status from file"""
    task_file = os.path.join(TASK_STORAGE_DIR, f"{task_id}.json")
    if not os.path.exists(task_file):
        return None
    
    with open(task_file, 'r') as f:
        return json.load(f)

def process_dataset_async(task_id, file_path, filename):
    """Process dataset in background thread"""
    try:
        # Update status to processing
        save_task_status(task_id, 'processing', {'message': 'Reading CSV file...'})
        
        # Read as DataFrame
        df = pd.read_csv(file_path)
        
        # Update status
        save_task_status(task_id, 'processing', {'message': 'Analyzing data quality...'})
        
        # Create output directory for profiler reports
        output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        
        # Run ObelixProfiler
        profiler = ObelixProfiler(df, output_dir)
        report_name, score, suggestions = profiler.run()
        
        # Save completed status with results
        save_task_status(task_id, 'completed', {
            'score': float(score),
            'suggestions': suggestions,
            'filename': filename,
            'report_url': os.path.join(settings.MEDIA_URL, "reports", f"{report_name}.html")
        })
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
            
    except Exception as e:
        # Save error status
        save_task_status(task_id, 'failed', {
            'error': f'Error processing file: {str(e)}'
        })
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass

@csrf_exempt
def home(request):
    """Render the main chatbot interface"""
    return render(request, 'home.html')

@csrf_exempt
def upload_dataset(request):
    """Handle CSV upload and start async processing"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    if 'dataset' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    uploaded_file = request.FILES['dataset']
    
    # Validate file type
    if not uploaded_file.name.endswith('.csv'):
        return JsonResponse({'error': 'Please upload a CSV file'}, status=400)
    
    try:
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Generate unique filename
        filename = f"{task_id}_{uploaded_file.name}"
        
        # Save file locally
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'datasets')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Initialize task status
        save_task_status(task_id, 'queued', {
            'filename': uploaded_file.name,
            'message': 'File uploaded, processing will begin shortly...'
        })
        
        # Start background processing
        thread = threading.Thread(
            target=process_dataset_async,
            args=(task_id, file_path, uploaded_file.name)
        )
        thread.daemon = True
        thread.start()
        
        return JsonResponse({
            'success': True,
            'task_id': task_id,
            'message': 'File uploaded successfully. Processing started.',
            'filename': uploaded_file.name
        })
        
    except Exception as e:
        return JsonResponse({'error': f'Error uploading file: {str(e)}'}, status=500)

@csrf_exempt
def check_status(request, task_id):
    """Check processing status of a task"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed'}, status=405)
    
    task_status = get_task_status(task_id)
    
    if not task_status:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
    # Clean up old task files (older than 1 hour)
    current_time = time.time()
    if current_time - task_status['timestamp'] > 3600:  # 1 hour
        task_file = os.path.join(TASK_STORAGE_DIR, f"{task_id}.json")
        try:
            os.remove(task_file)
        except:
            pass
        return JsonResponse({'error': 'Task expired'}, status=404)
    
    return JsonResponse({
        'task_id': task_id,
        'status': task_status['status'],
        'timestamp': task_status['timestamp'],
        **task_status['data']
    })