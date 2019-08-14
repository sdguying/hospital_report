from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Report, Entry
from .forms import ReportForm

# Create your views here.


def reports_index(request):
    """体检报告首页"""
    reports = Report.objects.all()

    # 添加新的报告
    if request.method != 'POST':
        form = ReportForm()
    else:
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reports:reports_index'))

    context = {
        'reports': reports,
        'form': form,
    }
    return render(request, 'reports/reports.html', context)


def show_report(request, report_id):
    """体检报告详细内容显示页面"""
    report = Report.objects.get(id=report_id)
    entries = Entry.objects.all()

    context = {
        'report': report,
        'entries': entries,
    }
    return render(request, 'reports/show_report.html', context)


