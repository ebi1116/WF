from django.db import migrations


PROJECTS = [
    {
        "title": "TURFiQ",
        "slug": "turfiq",
        "category": "website",
        "description": "Website project for TURFiQ.",
        "project_url": "https://turfiq.in",
        "display_order": 1,
        "is_published": True,
    },
    {
        "title": "SportIQ",
        "slug": "sportiq",
        "category": "website",
        "description": "Website project for SportIQ.",
        "project_url": "https://sportiq.co.in",
        "display_order": 2,
        "is_published": True,
    },
]


def add_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    for project in PROJECTS:
        Project.objects.get_or_create(slug=project["slug"], defaults=project)


def remove_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(slug__in=[project["slug"] for project in PROJECTS]).delete()


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0001_initial")]

    operations = [migrations.RunPython(add_projects, remove_projects)]
