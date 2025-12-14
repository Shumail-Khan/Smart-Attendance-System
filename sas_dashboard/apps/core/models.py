from django.db import models
from django.utils import timezone

STATUS_CHOICES = (
    ('online', 'online'),
    ('offline', 'offline'),
    ('error', 'error'),
)

MODEL_TYPE_CHOICES = (
    ('face_detection', 'face_detection'),
    ('face_recognition', 'face_recognition'),
    ('weapon_detection', 'weapon_detection'),
)

MODEL_FORMAT_CHOICES = (
    ('tensorrt', 'tensorrt'),
    ('onnx', 'onnx'),
    ('pytorch', 'pytorch'),
)

class PCConfiguration(models.Model):
    pc_id = models.CharField(max_length=20, primary_key=True)
    pc_name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    gpu_count = models.IntegerField(default=1)
    gpu_ids = models.CharField(max_length=50, default='0')
    is_active = models.BooleanField(default=True)
    last_heartbeat = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pc_configuration'

    def __str__(self):
        return f"{self.pc_id} - {self.pc_name}"


class AIModel(models.Model):
    id = models.AutoField(primary_key=True)
    model_type = models.CharField(max_length=30, choices=MODEL_TYPE_CHOICES)
    model_name = models.CharField(max_length=100)
    model_version = models.CharField(max_length=20, blank=True, null=True)
    model_path = models.CharField(max_length=500)
    model_format = models.CharField(max_length=20, choices=MODEL_FORMAT_CHOICES, default='tensorrt')
    input_size = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'ai_models'
        unique_together = ('model_type', 'model_name', 'model_version')
        indexes = [
            models.Index(fields=['model_type']),
        ]

    def __str__(self):
        return f"{self.model_type} - {self.model_name} : {self.model_version}"


class PcModelConfig(models.Model):
    id = models.AutoField(primary_key=True)
    pc = models.ForeignKey(PCConfiguration, on_delete=models.CASCADE, db_column='pc_id')
    model_type = models.CharField(max_length=30, choices=MODEL_TYPE_CHOICES)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, db_column='model_id')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pc_model_config'
        unique_together = ('pc', 'model_type')

    def __str__(self):
        return f"{self.pc.pc_id} : {self.model_type} -> {self.model.model_name}"
