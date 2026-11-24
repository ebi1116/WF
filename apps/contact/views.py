from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote as urlquote
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from .forms import ContactEnquiryForm, QuoteEnquiryForm
from .models import Quotation, QuotationItem


def contact(request):
    form = ContactEnquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks for getting in touch. Your enquiry has been received.")
        return redirect("contact:contact")
    return render(request, "public/contact.html", {"form": form})


def quote(request):
    form = QuoteEnquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        enquiry = form.save()
        return render(request, "public/quote_success.html", {"reference": enquiry.reference})
    return render(request, "public/quote.html", {"form": form})


def _quotation_login_required(request):
    if request.session.get("projects_authenticated"):
        return None
    login = reverse("portfolio:projects_login")
    return redirect(f"{login}?next={urlquote(request.get_full_path(), safe='/')}")


def quotation_dashboard(request):
    denied = _quotation_login_required(request)
    if denied:
        return denied
    quotes = Quotation.objects.all()
    return render(request, "private/quotations.html", {"quotations": quotes})


def quotation_create(request):
    denied = _quotation_login_required(request)
    if denied:
        return denied
    if request.method == "POST":
        descriptions = request.POST.getlist("item_description")
        quantities = request.POST.getlist("item_quantity")
        prices = request.POST.getlist("item_price")
        try:
            name = request.POST.get("customer_name", "").strip()
            if not name or not (len(descriptions) == len(quantities) == len(prices)):
                raise ValueError
            rows = []
            for desc, qty, price in zip(descriptions, quantities, prices):
                desc = desc.strip()
                if not desc and not qty and not price:
                    continue
                quantity, unit_price = Decimal(qty), Decimal(price)
                if not desc or len(desc) > 48 or not quantity.is_finite() or not unit_price.is_finite() or quantity <= 0 or unit_price < 0:
                    raise ValueError
                rows.append((desc, quantity, unit_price))
            discount = Decimal(request.POST.get("discount") or "0")
            tax_percent = Decimal(request.POST.get("tax_percent") or "0")
            issue_date = date.fromisoformat(request.POST.get("issue_date"))
            valid_until = date.fromisoformat(request.POST["valid_until"]) if request.POST.get("valid_until") else None
            if not rows or len(rows) > 12 or discount < 0 or not Decimal("0") <= tax_percent <= Decimal("100"):
                raise ValueError
            if valid_until and valid_until < issue_date:
                raise ValueError
            email = request.POST.get("customer_email", "").strip()
            if email:
                validate_email(email)
            quote = Quotation.objects.create(
                customer_name=name,
                customer_company=request.POST.get("customer_company", "").strip(),
                customer_email=email,
                customer_phone=request.POST.get("customer_phone", "").strip(),
                customer_address=request.POST.get("customer_address", "").strip(),
                issue_date=issue_date,
                valid_until=valid_until,
                discount=discount,
                tax_percent=tax_percent,
                notes=request.POST.get("notes", "").strip(),
            )
            QuotationItem.objects.bulk_create([
                QuotationItem(quotation=quote, description=desc, quantity=qty, unit_price=price, position=i)
                for i, (desc, qty, price) in enumerate(rows)
            ])
            messages.success(request, f"Quotation {quote.number} saved.")
            return redirect("contact:quotation_pdf", pk=quote.pk)
        except (ValueError, TypeError, InvalidOperation, KeyError, ValidationError):
            messages.error(request, "Check customer name, dates, and each item. Add 1 to 12 valid items.")
    return render(request, "private/quotation_form.html")


@require_GET
def quotation_pdf(request, pk):
    denied = _quotation_login_required(request)
    if denied:
        return denied
    quote = get_object_or_404(Quotation.objects.prefetch_related("items"), pk=pk)
    from .quotation_pdf import make_quotation_pdf
    response = HttpResponse(make_quotation_pdf(quote), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{quote.number}.pdf"'
    return response
