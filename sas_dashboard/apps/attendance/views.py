from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import AttendanceRecord, AttendanceSchedule
from .serializers import AttendanceRecordSerializer, AttendanceScheduleSerializer
from apps.persons.models import Person
from apps.cameras.models import TblCamera
from django.utils.timezone import now
from django.http import HttpResponse
import csv

def attendance_list_view(request):
    qs = AttendanceRecord.objects.select_related("person", "camera")

    # Filters
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    person_id = request.GET.get("person")
    camera_id = request.GET.get("camera")
    atype = request.GET.get("type")
    search = request.GET.get("search")

    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)
    if person_id:
        qs = qs.filter(person_id=person_id)
    if camera_id:
        qs = qs.filter(camera_id=camera_id)
    if atype:
        qs = qs.filter(attendance_type=atype)
    if search:
        qs = qs.filter(person_name__icontains=search)

    qs = qs.order_by("-timestamp")

    # Daily summary (today by default)
    today = now().date()
    summary_qs = AttendanceRecord.objects.filter(date=today)
    summary = {
        "in": summary_qs.filter(attendance_type="IN").count(),
        "out": summary_qs.filter(attendance_type="OUT").count(),
    }

    return render(request, "attendance/list.html", {
        "records": qs,
        "persons": Person.objects.all(),
        "cameras": TblCamera.objects.all(),
        "summary": summary,
    })

def attendance_create_view(request):
    if request.method == "POST":
        AttendanceRecord.objects.create(
            person_id=request.POST["person"],
            person_name=Person.objects.get(pid=request.POST["person"]).person_name,
            camera_id=request.POST["camera"],
            pc_id=request.POST.get("pc_id", ""),
            attendance_type=request.POST["attendance_type"],
            timestamp=request.POST["timestamp"],
            date=request.POST["timestamp"].split("T")[0],
        )
        return redirect("attendance_list")

    return render(request, "attendance/form.html", {
        "persons": Person.objects.all(),
        "cameras": TblCamera.objects.all(),
    })

def attendance_export_view(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Person", "Camera", "Type", "Timestamp", "Confidence"
    ])

    for r in AttendanceRecord.objects.all():
        writer.writerow([
            r.person_name,
            r.camera.location,
            r.attendance_type,
            r.timestamp,
            r.confidence,
        ])

    return response

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all().order_by("-timestamp")
    serializer_class = AttendanceRecordSerializer


class AttendanceScheduleViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSchedule.objects.all()
    serializer_class = AttendanceScheduleSerializer
