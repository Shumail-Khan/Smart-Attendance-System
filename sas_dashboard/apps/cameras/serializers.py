from rest_framework import serializers
from .models import TblCamera, CameraParameters, CameraPreset, CamPcConf

class TblCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblCamera
        fields = "__all__"


class CameraParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraParameters
        fields = "__all__"


class CameraPresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraPreset
        fields = "__all__"


class CamPcConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = CamPcConf
        fields = "__all__"
