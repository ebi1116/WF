from django.test import TestCase
from django.urls import reverse

from .models import ContactEnquiry, QuoteEnquiry


class EnquiryFormTests(TestCase):
    def test_contact_form_saves_valid_enquiry(self):
        response = self.client.post(reverse("contact:contact"), {
            "full_name": "Asha Example",
            "email": "asha@example.com",
            "phone": "",
            "service": "website",
            "subject": "New business website",
            "message": "We need a responsive site for our business.",
            "website": "",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your enquiry has been received.")
        self.assertEqual(ContactEnquiry.objects.count(), 1)

    def test_invalid_contact_form_is_not_saved(self):
        response = self.client.post(reverse("contact:contact"), {
            "full_name": "",
            "email": "not-an-email",
            "service": "website",
            "subject": "",
            "message": "",
            "website": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactEnquiry.objects.count(), 0)

    def test_honeypot_blocks_contact_spam(self):
        response = self.client.post(reverse("contact:contact"), {
            "full_name": "Spam Bot",
            "email": "bot@example.com",
            "service": "website",
            "subject": "Spam",
            "message": "Spam message",
            "website": "filled-in-by-bot",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactEnquiry.objects.count(), 0)

    def test_quote_request_saves_and_returns_unique_reference(self):
        response = self.client.post(reverse("contact:quote"), {
            "customer_name": "Asha Example",
            "email": "asha@example.com",
            "phone": "",
            "company_name": "",
            "service": "cloud",
            "budget": "discuss",
            "timeline": "flexible",
            "requirements": "We are planning a new cloud deployment for our application.",
            "website": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "public/quote_success.html")
        self.assertEqual(QuoteEnquiry.objects.count(), 1)
        enquiry = QuoteEnquiry.objects.get()
        self.assertEqual(len(enquiry.reference), 10)
        self.assertContains(response, enquiry.reference)
