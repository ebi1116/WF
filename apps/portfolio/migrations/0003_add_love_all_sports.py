from django.db import migrations


def add_love_all_sports(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.get_or_create(
        slug="loveallsports",
        defaults={
            "title": "Love All Sports",
            "category": "ecommerce",
            "description": "E-commerce website for Love All Sports.",
            "project_url": "https://loveallsports.net",
            "display_order": 3,
            "is_published": True,
        },
    )


def remove_love_all_sports(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(slug="loveallsports").delete()


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0003_clientproject")]
    operations = [migrations.RunPython(add_love_all_sports, remove_love_all_sports)]
