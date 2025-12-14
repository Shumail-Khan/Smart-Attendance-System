from django.db import models
from django.utils import timezone

class SystemMetrics(models.Model):
    id = models.BigAutoField(primary_key=True)
    pc_id = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    cpu_percent = models.FloatField(blank=True, null=True)
    cpu_temp_celsius = models.FloatField(blank=True, null=True)
    cpu_fan_rpm = models.IntegerField(blank=True, null=True)
    memory_percent = models.FloatField(blank=True, null=True)
    memory_used_mb = models.FloatField(blank=True, null=True)
    gpu_utilization = models.FloatField(blank=True, null=True)
    gpu_memory_percent = models.FloatField(blank=True, null=True)
    gpu_memory_used_mb = models.FloatField(blank=True, null=True)
    gpu_temp_celsius = models.FloatField(blank=True, null=True)
    gpu_fan_percent = models.FloatField(blank=True, null=True)
    gpu_power_watts = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'system_metrics'
        indexes = [
            models.Index(fields=['pc_id', 'timestamp'], name='idx_pc_timestamp'),
        ]

    def __str__(self):
        return f"{self.pc_id} @ {self.timestamp}"


class CameraMetrics(models.Model):
    id = models.BigAutoField(primary_key=True)
    camera = models.ForeignKey('cameras.TblCamera', on_delete=models.CASCADE, db_column='camera_id')
    pc_id = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    fps = models.FloatField(blank=True, null=True)
    avg_frame_time_ms = models.FloatField(blank=True, null=True)
    avg_detection_time_ms = models.FloatField(blank=True, null=True)
    avg_recognition_time_ms = models.FloatField(blank=True, null=True)
    frames_processed = models.BigIntegerField(blank=True, null=True)
    frames_dropped = models.BigIntegerField(blank=True, null=True)
    faces_detected = models.IntegerField(blank=True, null=True)
    faces_recognized = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=(('running','running'),('paused','paused'),('error','error'),('stopped','stopped')), blank=True, null=True)

    class Meta:
        db_table = 'camera_metrics'
        indexes = [
            models.Index(fields=['camera', 'timestamp'], name='idx_camera_timestamp'),
        ]

    def __str__(self):
        return f"{self.camera.camera_id} metrics @ {self.timestamp}"


class SystemAlerts(models.Model):
    id = models.BigAutoField(primary_key=True)
    pc_id = models.CharField(max_length=20, blank=True, null=True)
    camera_id = models.CharField(max_length=10, blank=True, null=True)
    timestamp = models.DateTimeField()
    level = models.CharField(max_length=10, choices=(('info','info'),('warning','warning'),('critical','critical')))
    category = models.CharField(max_length=20, choices=(('fps','fps'),('memory','memory'),('gpu','gpu'),('api','api'),('camera','camera'),('system','system')))
    message = models.TextField()
    value = models.FloatField(blank=True, null=True)
    threshold = models.FloatField(blank=True, null=True)
    is_acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.CharField(max_length=100, blank=True, null=True)
    acknowledged_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'system_alerts'
        indexes = [
            models.Index(fields=['timestamp'], name='idx_timestamp'),
            models.Index(fields=['level'], name='idx_level'),
            models.Index(fields=['is_acknowledged', 'timestamp'], name='idx_unacknowledged'),
        ]

    def __str__(self):
        return f"[{self.level}] {self.message[:80]}"
