from django.db import models
from django.urls import reverse


class Service(models.Model):
    class Category(models.TextChoices):
        WEBSITE = "website", "Website Development"
        ECOMMERCE = "ecommerce", "E-Commerce Development"
        CLOUD = "cloud", "Cloud Services"

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, unique=True)
    short_description = models.CharField(max_length=240)
    description = models.TextField()
    benefits = models.TextField(blank=True, help_text="One benefit per line.")
    features = models.TextField(blank=True, help_text="One feature per line.")
    technologies = models.CharField(max_length=300, blank=True, help_text="Comma-separated.")
    icon = models.CharField(max_length=60, default="fa-code", help_text="Font Awesome icon class, for example fa-code.")
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "title")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})

    @property
    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    @property
    def benefit_list(self):
        return [line.strip() for line in self.benefits.splitlines() if line.strip()]
