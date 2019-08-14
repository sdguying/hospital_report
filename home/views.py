from django.shortcuts import render
from reports.models import Report

# Create your views here.


def index(request):
    """home首页"""
    reports = Report.objects.all()

    context = {
        'reports': reports
    }
    return render(request, 'home/index.html', context)