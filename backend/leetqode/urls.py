"""
URL configuration for leetqode project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('allauth.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('problems.urls')),
    path('api/health/', views.health_check, name='health_check'),
    path('api/public/problems/', views.public_problems, name='public_problems'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
