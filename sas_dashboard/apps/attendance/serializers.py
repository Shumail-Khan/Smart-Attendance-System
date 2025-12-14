from rest_framework import serializers
from .models import AttendanceRecord, AttendanceSchedule

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = "__all__"


class AttendanceScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSchedule
        fields = "__all__"
