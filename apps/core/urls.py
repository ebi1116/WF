from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('', include('apps.services.urls')),
    path('', include('apps.portfolio.urls')),
    path('', include('apps.contact.urls')),
]
