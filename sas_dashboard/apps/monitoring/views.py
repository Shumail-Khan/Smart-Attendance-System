from rest_framework import viewsets
from .models import SystemMetrics, CameraMetrics, SystemAlerts
from .serializers import (
    SystemMetricsSerializer,
    CameraMetricsSerializer,
    SystemAlertsSerializer,
)

class SystemMetricsViewSet(viewsets.ModelViewSet):
    queryset = SystemMetrics.objects.all().order_by("-timestamp")
    serializer_class = SystemMetricsSerializer


class CameraMetricsViewSet(viewsets.ModelViewSet):
    queryset = CameraMetrics.objects.all().order_by("-timestamp")
    serializer_class = CameraMetricsSerializer


class SystemAlertsViewSet(viewsets.ModelViewSet):
    queryset = SystemAlerts.objects.all().order_by("-timestamp")
    serializer_class = SystemAlertsSerializer
