from django.db import models
from django.utils import timezone

class AttendanceRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey('persons.Person', on_delete=models.CASCADE, db_column='person_id')
    person_name = models.CharField(max_length=255)
    camera = models.ForeignKey('cameras.TblCamera', on_delete=models.CASCADE, db_column='camera_id')
    pc_id = models.CharField(max_length=20)
    attendance_type = models.CharField(max_length=3, choices=(('IN','IN'),('OUT','OUT')))
    confidence = models.FloatField(blank=True, null=True)
    image_path = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField()
    date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attendance_records'
        indexes = [
            models.Index(fields=['person', 'date'], name='idx_person_date'),
            models.Index(fields=['date'], name='idx_date'),
            models.Index(fields=['camera', 'date'], name='idx_camera_date'),
            models.Index(fields=['attendance_type', 'date'], name='idx_type_date'),
        ]

    def __str__(self):
        return f"{self.person_name} @ {self.timestamp} ({self.attendance_type})"


class AttendanceSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    in_time_start = models.TimeField()
    in_time_end = models.TimeField()
    out_time_start = models.TimeField(blank=True, null=True)
    out_time_end = models.TimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attendance_schedules'

    def __str__(self):
        return self.name
