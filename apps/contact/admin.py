from django.contrib import admin

from .models import ContactEnquiry, QuoteEnquiry


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "service", "subject", "created_at", "is_read")
    list_filter = ("service", "is_read", "created_at")
    search_fields = ("full_name", "email", "subject", "message")
    readonly_fields = ("created_at",)


@admin.register(QuoteEnquiry)
class QuoteEnquiryAdmin(admin.ModelAdmin):
    list_display = ("reference", "customer_name", "email", "service", "budget", "created_at", "is_read")
    list_filter = ("service", "budget", "timeline", "is_read", "created_at")
    search_fields = ("reference", "customer_name", "email", "company_name", "requirements")
    readonly_fields = ("reference", "created_at")
