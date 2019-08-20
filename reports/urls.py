"""
reports app's urls
"""

from django.urls import path
from . import views

urlpatterns = [
    path('reports_index.html', views.reports_index, name='reports_index'),
    path('<int:report_id>/show_report.html', views.show_report, name='show_report'),
    path('edit/<int:report_id>/edit_report_info.html', views.edit_report_info, name='edit_report_info'),
    path('del/<int:report_id>/del_report.html', views.del_report, name='del_report'),

    # 关于科室的编辑等路由
    path('edit/<int:report_id>/edit_global_category.html', views.edit_global_category, name='edit_global_category'),
    path('edit/<int:report_id>/<int:category_id>/edit_category.html', views.edit_category, name='edit_category'),
    path('del/<int:report_id>/<int:category_id>/del_category.html', views.del_category, name='del_category'),

    # 具体检查项目的路由
    path('del/<int:entry_id>/del_entry.html', views.del_entry, name='del_entry'),
    path('edit/<int:entry_id>/edit_entry.html', views.edit_entry, name='edit_entry'),

    # 删除一个科室包含下面所有检查项目的路由
    path('del/<int:report_id>/<int:category_id>/del_entries_of_category.html',
         views.del_entries_of_category, name='del_entries_of_category'),

    # 小结的相关路由
    path('add/<int:report_id>/<int:category_id>/add_summary.html', views.add_summary, name='add_summary'),
    path('del/<int:report_id>/<int:category_id>/del_summary.html', views.del_summary, name='del_summary'),
    path('edit/<int:report_id>/<int:category_id>/edit_summary.html', views.edit_summary, name='edit_summary'),

    # 总监报告路由
    path('add/<int:report_id>/add_conclusion.html', views.add_conclusion, name='add_conclusion'),
    path('edit/<int:report_id>/edit_conclusion.html', views.edit_conclusion, name='edit_conclusion'),
    path('del/<int:report_id>/del_conclusion.html', views.del_conclusion, name='del_conclusion'),
]