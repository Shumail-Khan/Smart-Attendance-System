from rest_framework import viewsets
from .models import TblCamera, CameraParameters, CameraPreset, CamPcConf
from .serializers import (
    TblCameraSerializer,
    CameraParametersSerializer,
    CameraPresetSerializer,
    CamPcConfSerializer,
)

class TblCameraViewSet(viewsets.ModelViewSet):
    queryset = TblCamera.objects.all()
    serializer_class = TblCameraSerializer
    lookup_field = "camera_id"


class CameraParametersViewSet(viewsets.ModelViewSet):
    queryset = CameraParameters.objects.all()
    serializer_class = CameraParametersSerializer


class CameraPresetViewSet(viewsets.ModelViewSet):
    queryset = CameraPreset.objects.all()
    serializer_class = CameraPresetSerializer


class CamPcConfViewSet(viewsets.ModelViewSet):
    queryset = CamPcConf.objects.all()
    serializer_class = CamPcConfSerializer
