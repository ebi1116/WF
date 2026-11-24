from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.views.defaults import server_error

from apps.portfolio.models import Project


class PublicPagesTests(TestCase):
    def test_public_pages_render(self):
        paths = [
            reverse("home"),
            reverse("about"),
            reverse("services:list"),
            reverse("services:detail", kwargs={"slug": "website-development"}),
            reverse("portfolio:list"),
            reverse("contact:contact"),
            reverse("contact:quote"),
            reverse("robots"),
            reverse("sitemap"),
        ]
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_home_uses_supplied_slider_images_and_lists_requested_projects(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "hero-workspace.png")
        self.assertContains(response, "hero-shopease.png")
        self.assertContains(response, "hero-cloud-server.png")
        self.assertContains(response, "TURFiQ")
        self.assertContains(response, "SportIQ")

    def test_portfolio_empty_state_and_category_filter(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("portfolio:list"))
        self.assertContains(response, "No published projects yet.")

        project = Project.objects.create(
            title="Example site",
            slug="example-site",
            category=Project.Category.WEBSITE,
            description="A project for checking portfolio routes.",
            is_published=True,
        )
        filtered = self.client.get(reverse("portfolio:list"), {"category": "website"})
        self.assertContains(filtered, project.title)
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 200)

    def test_requested_projects_have_working_detail_pages(self):
        for slug in ("turfiq", "sportiq"):
            with self.subTest(slug=slug):
                response = self.client.get(reverse("portfolio:detail", kwargs={"slug": slug}))
                self.assertEqual(response.status_code, 200)
                expected_domain = "turfiq.in" if slug == "turfiq" else "sportiq.co.in"
                self.assertContains(response, f"https://{expected_domain}")

    @override_settings(DEBUG=False, SECURE_SSL_REDIRECT=False)
    def test_custom_404_page(self):
        response = self.client.get("/this-page-does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "We couldn’t find that page.", status_code=404)

    def test_custom_500_template_renders(self):
        response = server_error(RequestFactory().get("/"))
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Something went wrong.", response.content)
