from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("projects/", views.projects_dashboard, name="projects"),
    path("projects/login/", views.projects_login, name="projects_login"),
    path("projects/logout/", views.projects_logout, name="projects_logout"),
    path("projects/add/", views.project_create, name="project_create"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),
    path("portfolio/", views.project_list, name="list"),
    path("portfolio/<slug:slug>/", views.project_detail, name="detail"),
]
