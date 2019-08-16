from django.contrib import admin
from reports.models import Report, Category, Entry, Conclusion, Summary

# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'work_unit', 'date', 'report_num', 'hospital')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_w')


class EntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'report', 'category', 'tips')


class SummaryAdmin(admin.ModelAdmin):
    list_display = ('content', 'report', 'category', 'doctor')


class ConclusionAdmin(admin.ModelAdmin):
    list_display = ('report', 'overview', 'summary_doctor', 'summary_date')


admin.site.register(Report, ReportAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Conclusion, ConclusionAdmin)