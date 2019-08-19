from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Report, Entry, Category, Summary
from .forms import ReportForm, CategoryForm_w, EntryForm, SummaryForm

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

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.report_id = report_id
            data.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report.id]))
    # 单一报告下所有的具体检查项目
    entries = Entry.objects.filter(report_id=report_id)
    categories = Category.objects.all()  # 所有的科室
    # set排序并去重，建立一个不重复的该报告有的所有科室id，作为字典的key
    category_id_list = list(set([entry.category_id for entry in entries]))

    # 通过entry.category_id找出该报告中有的科室名称放到列表中
    dicts ={}
    for category in categories:
        if category.id in category_id_list:
            # 把一个科室大类下的项目放到列表里
            entry_list = [ entry for entry in entries if entry.category_id == category.id ]
            # 科室名称作为key，该科室大类下的检查项目作为value，放入dicts，循环
            dicts[category.name] = entry_list
        else:
            continue

    # 小结的显示功能
    summaries = Summary.objects.filter(report_id=report_id)

    context = {
        'report': report,
        'dicts': dicts,
        'summaries': summaries,
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
        if not report.entry_set.all():
            report.delete()
            return HttpResponseRedirect(reverse('reports:reports_index'))
        else:
            message = '该报告下存在录入的内容，禁止删除，请逐个清理完相关内容后再行删除。'
            context = {
                'report': report,
                'message': message,
            }
            return render(request, 'reports/del_report.html', context)


def edit_global_category(request, report_id):
    """编辑全局科室"""
    categories = Category.objects.all()

    if request.method != 'POST':
        form = CategoryForm_w()
    else:
        form = CategoryForm_w(request.POST)
        if form.is_valid():
            form.save()
    context = {
        'categories': categories,
        'report_id': report_id,
        'form': form,
    }
    return render(request, 'reports/edit_global_category.html', context)


def edit_category(request, report_id, category_id):
    """修改科室名称"""
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = CategoryForm_w(instance=category)
    else:
        form = CategoryForm_w(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reports:edit_global_category', args=[report_id]))

    context = {
        'form': form,
        'category': category,
        'report_id': report_id,
    }
    return render(request, 'reports/edit_category.html', context)


def edit_entry(request, entry_id):
    """修改检查项目"""
    entry = Entry.objects.get(id=entry_id)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[entry.report_id]))

    context = {
        'form': form,
        'entry':entry,
    }
    return render(request, 'reports/edit_entry.html', context)


def del_category(request, report_id, category_id):
    """删除全局科室"""
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        context = {
            'category': category,
            'report_id': report_id,
        }
        return render(request, 'reports/del_category.html', context)
    else:
        try:
            category.delete()
        except:
            message = '该科室下存在具体体检项目，不允许删除！'
            context = {
                'message': message,
                'category': category,
                'report_id': report_id,
            }
            return render(request, 'reports/del_category.html', context)
        else: # 在try没有任何异常的时候执行
            return HttpResponseRedirect(reverse('reports:edit_global_category', args=[report_id]))


def del_entry(request, entry_id):
    """删除具体检查项目"""
    entry = Entry.objects.get(id=entry_id)

    if request.method != 'POST':
        context = {
            'entry': entry,
        }
        return render(request, 'reports/del_entry.html', context)
    else:
        entry.delete()
        return HttpResponseRedirect(reverse('reports:show_report', args=[entry.report_id]))


def find_category_name(x_id):
    """通过category.id查找category.name"""
    categories = Category.objects.all()
    for category in categories:
        if category.id == x_id:
            return category.name


def del_entries_of_category(request, report_id, category_id):
    """删除某个报告下面的整个科室下面的所有具体检查项目"""
    entries = Entry.objects.filter(report_id=report_id, category_id=category_id)
    report = Report.objects.get(id=report_id)

    category_name = find_category_name(category_id)

    if request.method != 'POST':
        context = {
            'entries': entries,
            'report': report,
            'category_id': category_id,
            'category_name': category_name,
        }
        return render(request, 'reports/del_entries_of_category.html', context)
    else:
        entries.delete()
        return HttpResponseRedirect(reverse('reports:show_report', args=[report_id]))


def add_summary(request, report_id, category_id):
    """添加小结"""
    report = Report.objects.get(id=report_id)
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = SummaryForm()
    else:
        form = SummaryForm(request.POST)
        if form.is_valid():
            summary_data = form.save(commit=False)
            summary_data.report_id = report.id
            summary_data.category_id = category.id
            summary_data.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report.id]))

    context = {
        'form': form,
        'report': report,
        'category': category,
    }
    return render(request, 'reports/add_summary.html', context)