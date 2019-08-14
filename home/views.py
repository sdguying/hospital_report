from django.shortcuts import render
from reports.models import Report

# Create your views here.


def index(request):
    """home首页"""

    return render(request, 'home/index.html')