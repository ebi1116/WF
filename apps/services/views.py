from django.shortcuts import get_object_or_404, render

from .models import Service


def service_list(request):
    return render(request, "public/services.html", {"services": Service.objects.filter(is_active=True)})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "public/service_detail.html", {
        "service": service,
        "related_services": Service.objects.filter(is_active=True).exclude(pk=service.pk),
    })
