import uuid
from decimal import Decimal

from django.db import models
from django.utils import timezone


class ContactEnquiry(models.Model):
    SERVICE_CHOICES = [
        ("website", "Website Development"),
        ("ecommerce", "E-Commerce Development"),
        ("cloud", "Cloud Services"),
        ("other", "Other / Not sure yet"),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.full_name} — {self.subject}"


class Quotation(models.Model):
    number = models.CharField(max_length=20, unique=True, editable=False)
    customer_name = models.CharField(max_length=160)
    customer_company = models.CharField(max_length=160, blank=True)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=40, blank=True)
    customer_address = models.TextField(blank=True)
    issue_date = models.DateField(default=timezone.localdate)
    valid_until = models.DateField(null=True, blank=True)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"Q-{timezone.localdate():%Y%m%d}-{uuid.uuid4().hex[:5].upper()}"
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return sum((item.amount for item in self.items.all()), Decimal("0.00"))

    @property
    def taxable_amount(self):
        return max(Decimal("0.00"), self.subtotal - self.discount)

    @property
    def tax_amount(self):
        return (self.taxable_amount * self.tax_percent / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def total(self):
        return self.taxable_amount + self.tax_amount

    def __str__(self):
        return f"{self.number} — {self.customer_name}"


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, related_name="items", on_delete=models.CASCADE)
    description = models.CharField(max_length=240)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("position", "id")

    @property
    def amount(self):
        return self.quantity * self.unit_price


class QuoteEnquiry(models.Model):
    SERVICE_CHOICES = ContactEnquiry.SERVICE_CHOICES[:3]
    BUDGET_CHOICES = [
        ("under-1k", "Under 1,000 (currency to discuss)"),
        ("1k-5k", "1,000 to 5,000 (currency to discuss)"),
        ("5k-10k", "5,000 to 10,000 (currency to discuss)"),
        ("10k-plus", "Over 10,000 (currency to discuss)"),
        ("discuss", "Let’s discuss"),
    ]
    TIMELINE_CHOICES = [
        ("urgent", "As soon as possible"),
        ("1-month", "Within 1 month"),
        ("1-3-months", "1–3 months"),
        ("flexible", "Flexible"),
    ]

    reference = models.CharField(max_length=12, unique=True, editable=False)
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    company_name = models.CharField(max_length=160, blank=True)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    budget = models.CharField(
        max_length=20,
        choices=BUDGET_CHOICES,
        help_text="The currency can be clarified when we follow up.",
    )
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} — {self.customer_name}"
