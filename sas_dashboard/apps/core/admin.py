from django.contrib import admin
from .models import PCConfiguration, AIModel, PcModelConfig

@admin.register(PCConfiguration)
class PCConfigurationAdmin(admin.ModelAdmin):
    list_display = ('pc_id', 'pc_name', 'status', 'ip_address', 'gpu_count', 'last_heartbeat')
    search_fields = ('pc_id', 'pc_name', 'ip_address')
    list_filter = ('status', 'is_active')

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('model_type', 'model_name', 'model_version', 'model_format', 'is_default', 'is_active')
    search_fields = ('model_name', 'model_version')
    list_filter = ('model_type', 'model_format', 'is_default', 'is_active')

@admin.register(PcModelConfig)
class PcModelConfigAdmin(admin.ModelAdmin):
    list_display = ('pc', 'model_type', 'model', 'is_active')
    list_filter = ('model_type', 'is_active')
