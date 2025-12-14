from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = "pid"

# # apps/persons/views.py
# import base64
# import requests
# from django.conf import settings
# from django.shortcuts import get_object_or_404
# from rest_framework import viewsets, status
# from rest_framework.decorators import action, api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .models import Person
# from .serializers import PersonSerializer, PersonCreateSerializer

# AI_BACKEND_ENROLL_URL = getattr(settings, 'AI_BACKEND_ENROLL_URL', 'http://localhost:8082/api/enroll/')

# class PersonViewSet(viewsets.ModelViewSet):
#     """
#     /api/persons/  - list, create
#     /api/persons/{pid}/ - retrieve, update, destroy
#     """
#     queryset = Person.objects.all().order_by('pid')
#     serializer_class = PersonSerializer
#     lookup_field = 'pid'
#     permission_classes = [IsAuthenticated]  # adjust per your auth setup

#     def get_serializer_class(self):
#         if self.action in ['create']:
#             return PersonCreateSerializer
#         return PersonSerializer

#     @action(detail=True, methods=['post'], url_path='enroll', permission_classes=[IsAuthenticated])
#     def enroll(self, request, pid=None):
#         """
#         Enroll endpoint - accept files (images) and send to AI backend.
#         AI backend is expected to return embedding string (space separated floats).
#         """
#         person = get_object_or_404(Person, pid=pid)
#         files = request.FILES.getlist('images')
#         if not files:
#             return Response({"detail": "No images provided. Provide images in 'images' multipart fields."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         # Prepare multipart form-data for AI backend
#         multipart = {}
#         files_payload = []
#         for i, f in enumerate(files):
#             # each file should be tuple: (fieldname, (filename, fileobj, content_type))
#             files_payload.append(('images', (f.name, f.read(), f.content_type or 'image/jpeg')))

#         data = {
#             'person_id': person.pid,
#             'person_name': person.person_name,
#         }

#         try:
#             resp = requests.post(AI_BACKEND_ENROLL_URL, data=data, files=files_payload, timeout=30)
#         except requests.RequestException as e:
#             return Response({"detail": "Error contacting AI backend", "error": str(e)},
#                             status=status.HTTP_502_BAD_GATEWAY)

#         if resp.status_code != 200:
#             return Response({"detail": "AI backend returned error", "status_code": resp.status_code, "body": resp.text},
#                             status=status.HTTP_502_BAD_GATEWAY)
#         try:
#             rjson = resp.json()
#         except ValueError:
#             return Response({"detail": "AI backend did not return JSON", "body": resp.text},
#                             status=status.HTTP_502_BAD_GATEWAY)

#         if not rjson.get('success'):
#             return Response({"detail": "AI backend enrollment failed", "body": rjson}, status=status.HTTP_400_BAD_REQUEST)

#         embedding = rjson.get('embedding')  # expected space-separated string of 128 floats
#         quality_score = rjson.get('quality_score', None)

#         if embedding:
#             person.person_embedding = embedding
#             person.save(update_fields=['person_embedding', 'updated_at'])

#         return Response({
#             "success": True,
#             "person_id": person.pid,
#             "embedding_saved": bool(embedding),
#             "quality_score": quality_score,
#             "ai_response": rjson
#         }, status=status.HTTP_200_OK)
