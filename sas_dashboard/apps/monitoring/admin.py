from django.contrib import admin
from .models import SystemMetrics, CameraMetrics, SystemAlerts

@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ("pc_id", "timestamp", "cpu_percent", "gpu_utilization")
    search_fields = ("pc_id",)
    list_filter = ("pc_id",)


@admin.register(CameraMetrics)
class CameraMetricsAdmin(admin.ModelAdmin):
    list_display = ("camera", "pc_id", "timestamp", "fps", "faces_detected")
    search_fields = ("camera__camera_id", "pc_id")
    list_filter = ("camera",)


@admin.register(SystemAlerts)
class SystemAlertsAdmin(admin.ModelAdmin):
    list_display = ("level", "category", "message", "timestamp", "is_acknowledged")
    list_filter = ("level", "category", "is_acknowledged")
    search_fields = ("message", "pc_id", "camera_id")
