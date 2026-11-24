from django.conf import settings


def business_contact(request):
    return {
        "contact_phone": settings.CONTACT_PHONE,
        "contact_email": settings.CONTACT_EMAIL,
    }
