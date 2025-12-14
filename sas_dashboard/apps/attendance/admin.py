from django.contrib import admin
from .models import AttendanceRecord, AttendanceSchedule

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("person_name", "person", "camera", "attendance_type", "timestamp")
    search_fields = ("person_name", "person__pid", "camera__camera_id")
    list_filter = ("attendance_type", "date")


@admin.register(AttendanceSchedule)
class AttendanceScheduleAdmin(admin.ModelAdmin):
    list_display = ("name", "in_time_start", "in_time_end", "out_time_start", "out_time_end", "is_active")
    list_filter = ("is_active",)
