# views.py
import os
import pandas as pd
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
from src import ObelixProfiler


@csrf_exempt
def home(request):
    """Render the main chatbot interface"""
    return render(request, 'home.html')


@csrf_exempt
def upload_dataset(request):
    """Handle CSV upload and profiling"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    if 'dataset' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    uploaded_file = request.FILES['dataset']

    # Validate file type
    if not uploaded_file.name.endswith('.csv'):
        return JsonResponse({'error': 'Please upload a CSV file'}, status=400)

    try:
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}_{uploaded_file.name}"

        # Save file locally
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'datasets')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Read as DataFrame
        df = pd.read_csv(file_path)
        df = df.sample(frac=0.005, random_state=42)

        # Create output directory for profiler reports
        output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        # os.makedirs(output_dir, exist_ok=True)
        # output_path = os.path.join(output_dir, unique_id)

        # Run ObelixProfiler
        profiler = ObelixProfiler(df, output_dir)
        report_name, score, suggestions = profiler.run()

        # Store results in session for later access
        # request.session['last_report'] = {
        #     'report_name': report_name,
        #     'score': float(score),
        #     'suggestions': suggestions,
        #     'filename': uploaded_file.name,
        #     'unique_id': unique_id
        # }

        return JsonResponse({
            'success': True,
            'score': float(score),
            'suggestions': suggestions,
            'filename': uploaded_file.name,
            'report_url': os.path.join(settings.MEDIA_URL, "reports", f"{report_name}.html")
            # f'/media/reports/{unique_id}.html'
        })

    except Exception as e:
        return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=500)