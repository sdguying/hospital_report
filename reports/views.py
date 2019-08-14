from django.shortcuts import render
from .models import Report

# Create your views here.


def reports_index(request):
    """体检报告首页"""
    reports = Report.objects.all()

    context = {
        'reports': reports,
    }
    return render(request, 'reports/reports.html', context)