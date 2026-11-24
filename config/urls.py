from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import include, path

from apps.core.sitemaps import PublicPageSitemap, ProjectSitemap

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': {'pages': PublicPageSitemap, 'projects': ProjectSitemap}}, name='sitemap'),
    path('robots.txt', lambda request: HttpResponse('User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n', content_type='text/plain'), name='robots'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
