"""
reports app's urls
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_index, name='reports_index')
]