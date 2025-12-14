from django.db import models
from django.utils import timezone

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    report_date = models.DateField()
    file_path = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "reports"

    def __str__(self):
        return self.title
