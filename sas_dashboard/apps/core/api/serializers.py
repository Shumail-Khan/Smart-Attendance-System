from rest_framework import serializers
from apps.core.models import PCConfiguration, AIModel, PcModelConfig

class PCConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCConfiguration
        fields = "__all__"

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = "__all__"

class PcModelConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PcModelConfig
        fields = "__all__"
