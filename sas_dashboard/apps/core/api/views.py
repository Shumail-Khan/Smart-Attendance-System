from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.core.models import PCConfiguration, AIModel, PcModelConfig
from apps.core.api.serializers import (
    PCConfigurationSerializer,
    AIModelSerializer,
    PcModelConfigSerializer
)

from apps.cameras.models import CamPcConf
from apps.cameras.serializers import CamPcConfSerializer


# -------------------------------
# PC MANAGEMENT
# -------------------------------
class PCConfigurationViewSet(viewsets.ModelViewSet):
    queryset = PCConfiguration.objects.all()
    serializer_class = PCConfigurationSerializer
    lookup_field = "pc_id"

    @action(detail=True, methods=["get"])
    def status(self, request, pc_id=None):
        pc = self.get_object()
        return Response({
            "pc_id": pc.pc_id,
            "status": pc.status,
            "last_heartbeat": pc.last_heartbeat
        })


# -------------------------------
# AI MODELS
# -------------------------------
class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

class PcModelConfigViewSet(viewsets.ModelViewSet):
    queryset = PcModelConfig.objects.all()
    serializer_class = PcModelConfigSerializer

# -------------------------------
# PC ↔ Model Assignment
# -------------------------------
class PcModelAssignmentViewSet(viewsets.ViewSet):

    def list(self, request, pc_id=None):
        items = PcModelConfig.objects.filter(pc_id=pc_id)
        return Response(PcModelConfigSerializer(items, many=True).data)

    def update(self, request, pc_id=None):
        PcModelConfig.objects.filter(pc_id=pc_id).delete()

        new_items = [
            PcModelConfig(
                pc_id=pc_id,
                model_type=item["model_type"],
                model_id=item["model_id"],
                is_active=True
            )
            for item in request.data
        ]
        PcModelConfig.objects.bulk_create(new_items)

        return Response({"status": "updated"})


# -------------------------------
# CAMERA ↔ PC Assignment
# -------------------------------
class CameraAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CamPcConf.objects.all()
    serializer_class = CamPcConfSerializer

    @action(detail=False, methods=["get"], url_path="pc/(?P<pc_id>[^/.]+)/cameras")
    def cameras_for_pc(self, request, pc_id=None):
        cams = CamPcConf.objects.filter(pc_id=pc_id)
        return Response(CamPcConfSerializer(cams, many=True).data)


# -------------------------------
# CONFIG SYNC
# -------------------------------
class ConfigSyncViewSet(viewsets.ViewSet):

    def create(self, request):
        return Response({"status": "sync triggered"})

    @action(detail=False, methods=["get"])
    def status(self, request):
        pcs = PCConfiguration.objects.values("pc_id", "status", "last_heartbeat")
        return Response(list(pcs))
