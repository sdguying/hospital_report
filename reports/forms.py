"""
reports表单
"""

from django import forms
from .models import Report


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