from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name='landing.html'), name='landing'),
    path("accounts/", include("accounts.urls")),     # accounts app moved to /accounts/
    path("tasks/", include(("tasks.urls", "tasks"), namespace="tasks")),  # add this line with namespace
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
