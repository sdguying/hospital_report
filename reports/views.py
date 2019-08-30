import pygal
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Report, Entry, Category, Summary, Conclusion
from .forms import ReportForm, CategoryForm, EntryForm, SummaryForm, ConclusionForm
from users.views import check_report_owner, check_category_owner


# Create your views here.


@login_required
def reports_index(request):
    """体检报告首页"""
    # 添加新的报告
    if request.method != 'POST':
        form = ReportForm()
    else:
        form = ReportForm(request.POST)
        if form.is_valid():
            new_report = form.save(commit=False)
            new_report.owner = request.user
            new_report.save()
            return HttpResponseRedirect(reverse('reports:reports_index'))

    reports = Report.objects.filter(owner=request.user).order_by('-date')

    context = {
        'reports': reports,
        'form': form,
    }
    return render(request, 'reports/reports_index.html', context)


@login_required
def show_report(request, report_id):
    """体检报告详细内容显示页面"""
    report = Report.objects.get(id=report_id)
    # 确认请求者是否为登录用户
    check_report_owner(request, report)
    # 所有的总检报告
    conclusion = Conclusion.objects.all()
    # 该报告下所有的具体检查项目
    entries = Entry.objects.filter(report_id=report_id)
    # 所有的该用户下的科室
    categories = Category.objects.filter(owner=request.user)

    # set排序并去重，建立一个不重复的该报告下所有科室id，作为字典的key
    category_id_list = list(set([entry.category_id for entry in entries]))

    # 通过entry.category_id找出该报告中有的科室名称放到列表中
    dicts = {}
    for category in categories:
        if category.id in category_id_list:
            # 把一个科室下的项目放到列表里
            entry_list = [entry for entry in entries if entry.category_id == category.id]
            # 科室名称作为key，该科室下的检查项目作为value，放入dicts，循环
            dicts[category.name] = entry_list
        else:
            continue

    # 添加具体检查项目的表单
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.report_id = report_id

            new_entry.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report.id]))

    # 小结的显示功能
    summaries = Summary.objects.filter(report_id=report_id)

    context = {
        'report': report,
        'categories': categories,
        'dicts': dicts,
        'summaries': summaries,
        'conclusion': conclusion,
        'form': form,
    }
    return render(request, 'reports/show_report.html', context)


@login_required
def edit_report_info(request, report_id):
    """修改报告基本信息"""
    report = Report.objects.get(id=report_id)
    # 确认请求者是否为登录用户
    check_report_owner(request, report)

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


@login_required
def del_report(request, report_id):
    """删除报告功能"""
    report = Report.objects.get(id=report_id)
    # 确认请求者是否为登录用户
    check_report_owner(request, report)

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


@login_required
def edit_global_category(request, report_id):
    """编辑全局科室"""
    report = Report.objects.get(id=report_id)
    # 确认请求者是否为登录用户
    check_report_owner(request, report)

    categories = Category.objects.filter(owner=request.user)

    if request.method != 'POST':
        form = CategoryForm()
    else:
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.owner = request.user
            new_category.save()

    context = {
        'categories': categories,
        'report': report,
        'form': form,
    }
    return render(request, 'reports/edit_global_category.html', context)


@login_required
def edit_category(request, report_id, category_id):
    """修改科室名称"""
    report = Report.objects.get(id=report_id)
    # 确认请求者是否为登录用户
    check_report_owner(request, report)

    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = CategoryForm(instance=category)
    else:
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reports:edit_global_category', args=[report.id]))

    context = {
        'form': form,
        'category': category,
        'report': report,
    }
    return render(request, 'reports/edit_category.html', context)


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def del_summary(request, report_id, category_id):
    """删除小结"""
    summary = Summary.objects.filter(report_id=report_id, category_id=category_id)
    report = Report.objects.get(id=report_id)
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        context = {
            'summary': summary,
            'report': report,
            'category': category,
        }
        return render(request, 'reports/del_summary.html', context)
    else:
        summary.delete()
        return HttpResponseRedirect(reverse('reports:show_report', args=[report_id]))


@login_required
def edit_summary(request, report_id, category_id):
    """修改小结"""
    summary = Summary.objects.get(report_id=report_id, category_id=category_id)
    report = Report.objects.get(id=report_id)
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = SummaryForm(instance=summary)
    else:
        form = SummaryForm(instance=summary, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report_id]))

    context = {
        'form': form,
        'report': report,
        'category': category,
    }
    return render(request, 'reports/edit_summary.html', context)


@login_required
def add_conclusion(request, report_id):
    """添加总检报告"""
    report = Report.objects.get(id=report_id)
    message = ''
    if request.method != 'POST':
        form = ConclusionForm()
    else:
        form = ConclusionForm(request.POST)
        conclusion = Conclusion.objects.all()
        if form.is_valid() and report_id not in [ con.report_id for con in conclusion ]:
            data = form.save(commit=False)
            data.report_id = report_id
            data.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report_id]))
        else:
            message = '该报告下已经存在总检报告，不允许再添加了'
    context = {
        'form': form,
        'report': report,
        'message': message,
    }
    return render(request, 'reports/add_conclusion.html', context)


@login_required
def edit_conclusion(request, report_id):
    """修改总检"""
    conclusion = Conclusion.objects.get(report_id=report_id)

    if request.method != 'POST':
        form = ConclusionForm(instance=conclusion)
    else:
        form = ConclusionForm(instance=conclusion, data=request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.report_id = report_id
            data.save()
            return HttpResponseRedirect(reverse('reports:show_report', args=[report_id]))

    context = {
        'form': form,
        'report_id': report_id,
    }
    return render(request, 'reports/edit_conclusion.html', context)


@login_required
def del_conclusion(request, report_id):
    """删除总检"""
    conclusion = Conclusion.objects.get(report_id=report_id)
    report = Report.objects.get(id=report_id)

    if request.method != 'POST':
        context = {
            'conclusion': conclusion,
            'report': report,
        }
        return render(request, 'reports/del_conclusion.html', context)
    else:
        conclusion.delete()
        return HttpResponseRedirect(reverse('reports:show_report', args=[report_id]))


"""
以下是数据图形化视图
"""


@login_required
def mat(request, entry_id):
    """entry的数据可视化视图"""
    # 选出模板中点选的某个具体的检查项目，然后把相同名字的项目都选出来
    entry = Entry.objects.get(id=entry_id)
    same_name_entries = Entry.objects.filter(name=entry.name).order_by('report_id')

    # 从这些相同名字的检查项目中做出两个列表，一个是检查结果的列表，一个是这些项目的所属报告的id列表
    entry_check_results_list = []
    reports_id = []
    for same_name_entry in same_name_entries:
        reports_id.append(same_name_entry.report_id)
        entry_check_results_list.append(same_name_entry.check_results)

    # 通过所属报告的id列表做出报告的标题的列表
    reports_title = []   # 在生成图像的时候，要用到的参数，x轴的labels
    for report_id in reports_id:
        report = Report.objects.get(id=report_id)
        reports_title.append(report.title)

    # 通过检查结果的列表筛选出是int或者float的数据，如果不是数字的不生成图像
    # reports_title列表中的报告和entry_check_results_list列表中的数据是一一对应的
    # 下面的代码是逐一转换entry_check_results_list列表中的元素，如果不能转换成整数且不能转换为浮点数，说明是文本
    # 则去掉该值，相应的reports_title列表中也要在相应的位置去掉一个值
    int_or_float_list = []   # 在生成图像的时候，要用到的参数，Y轴的数值
    count = len(entry_check_results_list) + 1
    for result in entry_check_results_list:
        count -= 1
        try:
            i_result = int(result)
        except:
            try:
                f_result = float(result)
            except:
                del reports_title[-count]
            else:
                int_or_float_list.append(f_result)
        else:
            int_or_float_list.append(i_result)

    # 生成图像
    if int_or_float_list:
        # pygal生成柱形图
        hist = pygal.Bar()

        hist.title = '历年报告' + str(entry.name) + '的指标柱形图'
        hist.x_labels = reports_title
        hist.x_title = '年份'
        hist.y_title = '数值'

        hist.add('指标', int_or_float_list)
        hist.render_to_file('static/images/reports/{id}.svg'.format(id=entry.id))

        context = {
            'entry': entry,
        }
        return render(request, 'reports/show_mat.html', context)
    else:
        return HttpResponseRedirect(reverse('reports:show_report', args=[entry.report_id]))
