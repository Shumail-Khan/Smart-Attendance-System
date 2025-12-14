from rest_framework import viewsets
from .models import AttendanceRecord, AttendanceSchedule
from .serializers import AttendanceRecordSerializer, AttendanceScheduleSerializer

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all().order_by("-timestamp")
    serializer_class = AttendanceRecordSerializer


class AttendanceScheduleViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSchedule.objects.all()
    serializer_class = AttendanceScheduleSerializer
