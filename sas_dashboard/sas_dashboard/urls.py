from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings

# PERSONS
from apps.persons.views import PersonViewSet
from apps.persons.views import (
    person_list_view,
    person_detail_view,
    person_create_view,
    person_edit_view,
)


# CAMERAS
from apps.cameras.views import (
    TblCameraViewSet,
    CameraParametersViewSet,
    CameraPresetViewSet,
    CamPcConfViewSet,
)
from apps.cameras.views import (
    camera_grid_view,
    camera_detail_view,
    camera_config_view,
)

# ATTENDANCE
from apps.attendance.views import AttendanceRecordViewSet, AttendanceScheduleViewSet
from apps.attendance.views import (
    attendance_list_view,
    attendance_create_view,
    attendance_export_view,
)

# MONITORING
from apps.monitoring.views import (
    SystemMetricsViewSet,
    CameraMetricsViewSet,
    SystemAlertsViewSet,
)

# REPORTS
from apps.reports.views import ReportViewSet

# CORE
from apps.core.api.views import (
    PCConfigurationViewSet,
    AIModelViewSet,
    PcModelAssignmentViewSet,
    CameraAssignmentViewSet,
    ConfigSyncViewSet,
)
from apps.core.views import dashboard

router = DefaultRouter()

# PERSONS
router.register("persons", PersonViewSet)

# CAMERAS
router.register("cameras", TblCameraViewSet)
router.register("camera-parameters", CameraParametersViewSet)
router.register("camera-presets", CameraPresetViewSet)
router.register("cam-pc-conf", CamPcConfViewSet)

# ATTENDANCE
router.register("attendance-records", AttendanceRecordViewSet)
router.register("attendance-schedules", AttendanceScheduleViewSet)

# MONITORING
router.register("system-metrics", SystemMetricsViewSet)
router.register("camera-metrics", CameraMetricsViewSet)
router.register("system-alerts", SystemAlertsViewSet)

# REPORTS
router.register("reports", ReportViewSet)

router.register("pcs", PCConfigurationViewSet, basename="pcs")
router.register("models", AIModelViewSet, basename="models")
router.register("assignments", CameraAssignmentViewSet, basename="assignments")
router.register("sync", ConfigSyncViewSet, basename="sync")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("", dashboard, name="dashboard"),
    path("persons/", person_list_view, name="person_list"),
    path("persons/add/", person_create_view, name="person_add"),
    path("persons/<str:pid>/", person_detail_view, name="person_detail"),
    path("persons/<str:pid>/edit/", person_edit_view, name="person_edit"),
    path("cameras/", camera_grid_view, name="camera_grid"),
    path("cameras/<str:camera_id>/", camera_detail_view, name="camera_detail"),
    path("cameras/<str:camera_id>/config/", camera_config_view, name="camera_config"),
    path("attendance/", attendance_list_view, name="attendance_list"),
    path("attendance/add/", attendance_create_view, name="attendance_add"),
    path("attendance/export/", attendance_export_view, name="attendance_export"),
]
if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]