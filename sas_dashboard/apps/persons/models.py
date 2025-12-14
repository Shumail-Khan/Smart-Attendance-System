from django.db import models
from django.utils import timezone
import numpy as np

class Person(models.Model):
    pid = models.CharField(max_length=50, primary_key=True)  # e.g., "25"
    person_name = models.CharField(max_length=255)
    person_nic = models.CharField(max_length=20, blank=True, null=True)
    person_father = models.CharField(max_length=255, blank=True, null=True)
    person_designation = models.CharField(max_length=100, blank=True, null=True)
    person_cat = models.CharField(max_length=50, blank=True, null=True)
    person_embedding = models.TextField()  # space-separated 128 floats
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'person'

    def __str__(self):
        return f"{self.pid} - {self.person_name}"

    def get_embedding_array(self):
        if not self.person_embedding:
            return None
        return np.array([float(x) for x in self.person_embedding.strip().split()])

    def set_embedding_array(self, arr):
        self.person_embedding = ' '.join([str(float(x)) for x in arr])
