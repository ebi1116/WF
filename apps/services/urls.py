from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("services/", views.service_list, name="list"),
    path("services/<slug:slug>/", views.service_detail, name="detail"),
]
