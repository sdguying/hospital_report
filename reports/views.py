from django.shortcuts import render
from .models import Report

# Create your views here.


def index(request):
    """首页"""
    return render(request, 'index.html')


def reports_index(request):
    report = Report.objects.all()

    context = {
        'report': report,
    }
    return render(request, 'reports/reports.html', context)