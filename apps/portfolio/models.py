from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Project(models.Model):
    class Category(models.TextChoices):
        WEBSITE = "website", "Website Development"
        ECOMMERCE = "ecommerce", "E-Commerce"
        CLOUD = "cloud", "Cloud Services"

    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    description = models.TextField()
    thumbnail = models.FileField(
        upload_to="portfolio/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    project_url = models.URLField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("display_order", "-created_at")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("portfolio:detail", kwargs={"slug": self.slug})


class ClientProject(models.Model):
    """Private project and financial tracking, separate from the public portfolio."""
    name = models.CharField(max_length=160)
    client = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    total_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_received = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-start_date", "-created_at")

    @property
    def profit(self):
        return self.total_payment - self.expenses

    @property
    def balance_due(self):
        return self.total_payment - self.amount_received

    def __str__(self):
        return self.name
