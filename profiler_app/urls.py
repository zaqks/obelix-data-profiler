# urls.py (app level)
from django.urls import path
from . import views

app_name = 'profiler'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_dataset, name='upload_dataset')    
]
