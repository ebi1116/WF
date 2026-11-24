import hmac

from django.conf import settings
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import ClientProject, Project


def project_list(request):
    projects = Project.objects.filter(is_published=True)
    category = request.GET.get("category", "")
    if category in Project.Category.values:
        projects = projects.filter(category=category)
    return render(request, "public/portfolio.html", {"projects": projects, "active_category": category})


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return render(request, "public/project_detail.html", {"project": project})


def projects_dashboard(request):
    if not request.session.get("projects_authenticated"):
        return redirect("portfolio:projects_login")
    projects = ClientProject.objects.all()
    totals = {
        "payment": sum((p.total_payment for p in projects), 0),
        "received": sum((p.amount_received for p in projects), 0),
        "profit": sum((p.profit for p in projects), 0),
    }
    return render(request, "private/projects.html", {"projects": projects, "totals": totals})


def projects_login(request):
    if request.session.get("projects_authenticated"):
        return redirect("portfolio:projects")
    error = False
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if (hmac.compare_digest(username, settings.PROJECTS_USERNAME)
                and hmac.compare_digest(password, settings.PROJECTS_PASSWORD)
                and settings.PROJECTS_PASSWORD != "change-this-password"):
            request.session.cycle_key()
            request.session["projects_authenticated"] = True
            next_url = request.POST.get("next", "")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_url)
            return redirect("portfolio:projects")
        error = True
    return render(request, "private/projects_login.html", {"error": error, "next": request.GET.get("next", "")})


@require_POST
def projects_logout(request):
    request.session.pop("projects_authenticated", None)
    return redirect("portfolio:projects_login")


def project_create(request):
    if not request.session.get("projects_authenticated"):
        return redirect("portfolio:projects_login")
    if request.method == "POST":
        fields = {key: request.POST.get(key, "").strip() for key in
                  ("name", "client", "description", "total_payment", "amount_received", "expenses", "start_date", "end_date")}
        try:
            from datetime import date
            from decimal import Decimal, InvalidOperation
            project = ClientProject(
                name=fields["name"], client=fields["client"], description=fields["description"],
                total_payment=Decimal(fields["total_payment"] or "0"),
                amount_received=Decimal(fields["amount_received"] or "0"),
                expenses=Decimal(fields["expenses"] or "0"),
                start_date=date.fromisoformat(fields["start_date"]) if fields["start_date"] else None,
                end_date=date.fromisoformat(fields["end_date"]) if fields["end_date"] else None,
            )
            if not project.name or min(project.total_payment, project.amount_received, project.expenses) < 0:
                raise ValueError
            project.save()
            messages.success(request, "Project saved successfully.")
            return redirect("portfolio:projects")
        except (ValueError, InvalidOperation):
            messages.error(request, "Enter a project name, valid dates, and non-negative amounts.")
            return render(request, "private/project_form.html", {"values": fields})
    return render(request, "private/project_form.html")


@require_POST
def project_delete(request, pk):
    if not request.session.get("projects_authenticated"):
        return redirect("portfolio:projects_login")
    ClientProject.objects.filter(pk=pk).delete()
    messages.success(request, "Project deleted.")
    return redirect("portfolio:projects")
