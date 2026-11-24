from django.urls import path

from . import views

app_name = "contact"

urlpatterns = [
    path("quotation", views.quotation_dashboard),
    path("quotation/", views.quotation_dashboard, name="quotation_dashboard"),
    path("quotation/create/", views.quotation_create, name="quotation_create"),
    path("quotation/<int:pk>/pdf/", views.quotation_pdf, name="quotation_pdf"),
    path("contact/", views.contact, name="contact"),
    path("get-a-quote/", views.quote, name="quote"),
]
