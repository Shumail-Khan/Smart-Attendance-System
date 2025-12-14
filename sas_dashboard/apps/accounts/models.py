from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin','admin'),
        ('manager','manager'),
        ('viewer','viewer'),
    )

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    department = models.CharField(max_length=100, blank=True, null=True)
    can_manage_persons = models.BooleanField(default=False)
    can_manage_cameras = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=True)
    can_export_data = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return f"{self.user.username} ({self.role})"
