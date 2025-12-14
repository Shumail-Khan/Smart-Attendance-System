from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "report_date", "created_at")
    search_fields = ("title",)
