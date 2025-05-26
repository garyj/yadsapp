# URL Configuration
# https://docs.djangoproject.com/en/5.2/topics/http/urls/

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Out urls
    path('', TemplateView.as_view(template_name='base.html')),
    # Admin area
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
