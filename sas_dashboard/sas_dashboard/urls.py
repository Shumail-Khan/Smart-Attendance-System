from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings

# PERSONS
from apps.persons.views import PersonViewSet

# CAMERAS
from apps.cameras.views import (
    TblCameraViewSet,
    CameraParametersViewSet,
    CameraPresetViewSet,
    CamPcConfViewSet,
)

# ATTENDANCE
from apps.attendance.views import AttendanceRecordViewSet, AttendanceScheduleViewSet

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
]
if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]