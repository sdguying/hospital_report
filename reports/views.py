from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Report, Entry, Category
from .forms import ReportForm, CategoryForm, EntryForm

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
    return render(request, 'reports/reports_index.html', context)


def show_report(request, report_id):
    """体检报告详细内容显示页面"""
    report = Report.objects.get(id=report_id)
    category = Category.objects.all()
    entries = Entry.objects.all()

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            # if form not in [x for x in category]:
            data = form.save(commit=False)
            data.report_id = report_id
            data.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report.id]))

    context = {
        'report': report,
        'entries': entries,
        'form': form,
    }
    return render(request, 'reports/show_report.html', context)


def edit_report_info(request, report_id):
    """修改报告基本信息"""
    report = Report.objects.get(id=report_id)

    if request.method != 'POST':
        form = ReportForm(instance=report)
    else:
        form = ReportForm(instance=report, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report.id]))

    context = {
        'form': form,
        'report': report,
    }
    return render(request, 'reports/edit_report_info.html', context)


def del_report(request, report_id):
    """删除报告功能"""
    report = Report.objects.get(id=report_id)

    if request.method != 'POST':
        context = {
            'report': report,
        }
        return render(request, 'reports/del_report.html', context)
    else:
        report.delete()
        return HttpResponseRedirect(reverse('reports:reports_index'))



