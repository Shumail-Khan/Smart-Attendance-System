from rest_framework import viewsets
from .models import TblCamera, CameraParameters, CameraPreset, CamPcConf
from django.shortcuts import render, get_object_or_404
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

def camera_grid_view(request):
    cameras = TblCamera.objects.all()
    return render(request, "cameras/grid.html", {"cameras": cameras})


def camera_detail_view(request, camera_id):
    camera = get_object_or_404(TblCamera, camera_id=camera_id)
    params = CameraParameters.objects.filter(camera_id=camera).first()
    return render(request, "cameras/detail.html", {
        "camera": camera,
        "params": params,
    })


def camera_config_view(request, camera_id):
    camera = get_object_or_404(TblCamera, camera_id=camera_id)
    params, _ = CameraParameters.objects.get_or_create(camera_id=camera)

    if request.method == "POST":
        params.ip_address = request.POST["ip_address"]
        params.username = request.POST["username"]
        params.password = request.POST["password"]
        params.cam_type = request.POST["cam_type"]
        params.fr_conf_thresh = request.POST["fr_conf_thresh"]
        params.fr_iou_thresh = request.POST["fr_iou_thresh"]
        params.recognition_t = request.POST["recognition_t"]
        params.fr_min_frame_count = request.POST["fr_min_frame_count"]
        params.save()

    return render(request, "cameras/config.html", {
        "camera": camera,
        "params": params
    })