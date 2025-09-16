from django.urls import path
from .views import profiler_app

urlpatterns = [
    path('', profiler_app, name='profiler_app'),
]
