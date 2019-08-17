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
    path('add_new_category.html', views.add_new_category, name='add_new_category'),
]