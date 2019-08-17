from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Report, Entry, Category
from .forms import ReportForm, CategoryForm_w, EntryForm

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
    # entries = Entry.objects.all()

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.report_id = report_id
            data.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report.id]))

    entries = Entry.objects.filter(report_id=report_id)
    categories = Category.objects.all()
    #
    category_id_list = list(set([ entry.id for entry in entries ]))
    # 找出该报告中有的科室放到列表中
    category_name_list = []
    for category in categories:
        if category.id in category_id_list:
            category_name_list.append(category.name)

    context = {
        'report': report,
        'entries': entries,
        'category_name_list': category_name_list,
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


def add_new_category(request):
    """新增科室"""
    categories = Category.objects.all()

    if request.method != 'POST':
        form = CategoryForm_w()
    else:
        form = CategoryForm_w(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'reports/add_new_category.html', context)


def edit_category(request, category_id):
    """修改科室名称"""
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = CategoryForm_w(instance=category)
    else:
        form = CategoryForm_w(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reports:add_new_category'))

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'reports/edit_category.html', context)


def del_category(request, category_id):
    """删除科室"""
    category = Category.objects.get(id=category_id)
    message = ''

    if request.method != 'POST':
        context = {
            'category': category,
            'message': message,
        }
        return render(request, 'reports/del_category.html', context)
    else:
        try:
            category.delete()
        except:
            message = '该科室下存在具体体检项目，不允许删除！'
            context = {'message': message, 'category': category}
            return render(request, 'reports/del_category.html', context)
        else: # 在try没有任何异常的时候执行
            return HttpResponseRedirect(reverse('reports:add_new_category'))



