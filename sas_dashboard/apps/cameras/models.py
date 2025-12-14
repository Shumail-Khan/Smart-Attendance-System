from django.db import models
from django.utils import timezone

ATTENDANCE_TYPE_CHOICES = (
    ('IN', 'IN'),
    ('OUT', 'OUT'),
)

CAM_TYPE_CHOICES = (
    ('PTZ', 'PTZ'),
    ('Fixed', 'Fixed'),
)

DIST_METHOD_CHOICES = (
    ('cosine', 'cosine'),
    ('euclidean', 'euclidean'),
)

NORM_METHOD_CHOICES = (
    ('fixed', 'fixed'),
    ('l2', 'l2'),
)

class TblCamera(models.Model):
    camera_id = models.CharField(max_length=10, primary_key=True)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    attendance_type = models.CharField(max_length=3, choices=ATTENDANCE_TYPE_CHOICES, default='IN')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'tbl_camera'

    def __str__(self):
        return f"{self.camera_id} - {self.location}"


class CameraParameters(models.Model):
    camera_id = models.OneToOneField(TblCamera, on_delete=models.CASCADE, primary_key=True, db_constraint=False)
    ip_address = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    cam_type = models.CharField(max_length=20, choices=CAM_TYPE_CHOICES)

    # FR parameters
    fr_conf_thresh = models.FloatField(default=0.32)
    fr_iou_thresh = models.FloatField(default=0.3)
    fr_min_avg_thresh = models.FloatField(default=0.5)
    fr_min_frame_count = models.IntegerField(default=10)
    fr_min_frame_count_2 = models.IntegerField(default=30)
    fr_api_counter = models.IntegerField(default=1)

    recognition_t = models.FloatField(default=0.32)
    dist_method = models.CharField(max_length=20, choices=DIST_METHOD_CHOICES, default='cosine')
    norm_method = models.CharField(max_length=20, choices=NORM_METHOD_CHOICES, default='fixed')

    _sd = models.CharField(max_length=50, blank=True, null=True)
    _flag = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'camera_parameters'

    def __str__(self):
        return f"Params for {self.camera_id}"


class CameraPreset(models.Model):
    id = models.AutoField(primary_key=True)
    camera = models.ForeignKey(TblCamera, on_delete=models.CASCADE, related_name='presets')
    preset_token = models.CharField(max_length=10)
    preset_name = models.CharField(max_length=100, blank=True, null=True)
    preset_time = models.IntegerField(default=5)     # minutes
    preset_delay = models.IntegerField(default=0)    # seconds
    preset_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'camera_presets'
        unique_together = ('camera', 'preset_token')
        indexes = [
            models.Index(fields=['camera']),
            models.Index(fields=['camera', 'preset_order']),
        ]

    def __str__(self):
        return f"{self.camera.camera_id} preset {self.preset_token}"


class CamPcConf(models.Model):
    id = models.AutoField(primary_key=True)
    pc_id = models.CharField(max_length=20)
    cam = models.ForeignKey(TblCamera, on_delete=models.CASCADE, db_column='cam_id')
    gpu_id = models.IntegerField(default=0)

    enable_face_recognition = models.BooleanField(default=True)
    enable_weapon_detection = models.BooleanField(default=False)
    enable_tracking = models.BooleanField(default=True)
    enable_live_stream = models.BooleanField(default=True)

    priority = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cam_pc_conf'
        unique_together = ('pc_id', 'cam')
        indexes = [
            models.Index(fields=['pc_id', 'gpu_id']),
        ]

    def __str__(self):
        return f"{self.pc_id} -> {self.cam.camera_id} (GPU {self.gpu_id})"
