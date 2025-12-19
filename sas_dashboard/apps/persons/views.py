from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import default_storage
from django.conf import settings
import os


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = "pid"
def person_list_view(request):
    persons = Person.objects.all().order_by("-created_at")
    return render(request, "persons/list.html", {"persons": persons})


def person_detail_view(request, pid):
    person = get_object_or_404(Person, pid=pid)
    return render(request, "persons/detail.html", {"person": person})


def person_create_view(request):
    if request.method == "POST":
        person = Person.objects.create(
            pid=request.POST["pid"],
            person_name=request.POST["person_name"],
            person_nic=request.POST.get("person_nic"),
            person_father=request.POST.get("person_father"),
            person_designation=request.POST.get("person_designation"),
            person_cat=request.POST.get("person_cat"),
            person_embedding="",  # filled later
        )

        photo = request.FILES.get("profile_photo")
        if photo:
            path = os.path.join("person_photos", f"{person.pid}.jpg")
            default_storage.save(path, photo)

        return redirect("person_list")

    return render(request, "persons/form.html", {"mode": "create"})

def person_edit_view(request, pid):
    person = get_object_or_404(Person, pid=pid)

    if request.method == "POST":
        person.person_name = request.POST["person_name"]
        person.person_designation = request.POST.get("person_designation")
        person.person_cat = request.POST.get("person_cat")
        person.save()

        photo = request.FILES.get("profile_photo")
        if photo:
            path = os.path.join("person_photos", f"{person.pid}.jpg")
            default_storage.save(path, photo)

        return redirect("person_detail", pid=pid)

    return render(request, "persons/form.html", {
        "mode": "edit",
        "person": person
    })
