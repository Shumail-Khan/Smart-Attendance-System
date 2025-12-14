from rest_framework import serializers
from .models import SystemMetrics, CameraMetrics, SystemAlerts

class SystemMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMetrics
        fields = "__all__"


class CameraMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraMetrics
        fields = "__all__"


class SystemAlertsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemAlerts
        fields = "__all__"
