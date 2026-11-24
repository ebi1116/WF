from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.portfolio.models import Project


class PublicPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return ["home", "about", "services:list", "portfolio:list", "contact:contact", "contact:quote"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Project.objects.filter(is_published=True)
