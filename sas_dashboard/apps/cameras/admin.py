from django.contrib import admin
from .models import TblCamera, CameraParameters, CameraPreset, CamPcConf

@admin.register(TblCamera)
class TblCameraAdmin(admin.ModelAdmin):
    list_display = ("camera_id", "location", "attendance_type", "is_active", "created_at")
    search_fields = ("camera_id", "location")
    list_filter = ("attendance_type", "is_active")


@admin.register(CameraParameters)
class CameraParametersAdmin(admin.ModelAdmin):
    list_display = ("camera_id", "ip_address", "username", "cam_type", "created_at")
    search_fields = ("camera_id__camera_id", "ip_address")
    list_filter = ("cam_type",)


@admin.register(CameraPreset)
class CameraPresetAdmin(admin.ModelAdmin):
    list_display = ("camera", "preset_token", "preset_name", "preset_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("camera__camera_id", "preset_token")


@admin.register(CamPcConf)
class CamPcConfAdmin(admin.ModelAdmin):
    list_display = ("pc_id", "cam", "gpu_id", "enable_face_recognition", "is_active")
    list_filter = ("enable_face_recognition", "enable_weapon_detection", "is_active")
    search_fields = ("pc_id", "cam__camera_id")
