from django.contrib import admin
from reports.models import Report, Entry, Conclusion, Summary

# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'work_unit', 'date', 'report_num', 'hospital')

class EntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'report', 'category', 'tips')

class SummaryAdmin(admin.ModelAdmin):
    list_display = ('content', 'report', 'category', 'doctor')

admin.site.register(Report, ReportAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Conclusion)