from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("pid", "person_name", "person_designation", "person_cat", "created_at")
    search_fields = ("pid", "person_name", "person_nic")
