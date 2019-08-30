"""
reports表单
"""

from django import forms
from .models import Report, Category, Entry, Summary, Conclusion


class ReportForm(forms.ModelForm):
    """报告的表单"""
    class Meta:
        model = Report
        fields = [
            'title',
            'report_num',
            'name',
            'sex',
            'age',
            'work_unit',
            'hospital',
            'date',
        ]
        labels = {
            'title': '标题',
            'report_num': '报告编号',
            'name': '姓名',
            'sex': '性别',
            'age': '年龄',
            'work_unit': '工作单位',
            'hospital': '医院',
            'date': '日期',
        }


# class CategoryForm_select(forms.Form):
#     """为category模型作一个动态的下拉框"""
#     category = forms.ChoiceField(label='科室')
#
#     def __init__(self, *args, **kwargs):
#         """"""
#         super(CategoryForm_select, self).__init__(*args, **kwargs)
#         self.fields['category'].choices = (( x.name ) for x in Category.objects.all())


class CategoryForm(forms.ModelForm):
    """科室表单"""
    class Meta:
        model = Category
        fields = [
            'name',
        ]
        labels = {
            'name': '填入科室'
        }


class EntryForm(forms.ModelForm):
    """具体项目表单"""
    class Meta:
        model = Entry
        fields = [
            # 'category',
            'name',
            'check_results',
            'unit',
            'reference_range',
            'tips',
        ]
        labels = {
            # 'category': '所属科室',
            'name': '项目名称',
            'check_results': '检查结果',
            'unit': '单位',
            'reference_range': '参考范围',
            'tips': '提示',
        }


class SummaryForm(forms.ModelForm):
    """小结表单"""
    class Meta:
        model = Summary
        fields = [
            'content',
            'doctor',
        ]
        labels = {
            'content': '小结内容',
            'doctor': '小结医生'
        }


class ConclusionForm(forms.ModelForm):
    """总检报告表单"""
    class Meta:
        model = Conclusion
        fields = [
            'overview',
            'proposal',
            'summary_date',
            'summary_doctor',
        ]
        labels = {
            'overview': '综述',
            'proposal': '建议',
            'summary_date': '时间',
            'summary_doctor': '总检医生',
        }