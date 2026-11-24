from django.shortcuts import render

from apps.portfolio.models import Project
from apps.services.models import Service


def home(request):
    return render(request, "public/home.html", {
        "services": Service.objects.filter(is_active=True),
        "projects": Project.objects.filter(is_published=True)[:3],
    })


def about(request):
    return render(request, "public/about.html")
