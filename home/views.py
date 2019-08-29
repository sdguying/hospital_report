from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from reports.models import Report

# Create your views here.


@login_required
def index(request):
    """home首页"""

    return render(request, 'home/index.html')