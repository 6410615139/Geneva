from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path("", map_view, name="map_view"),
    path('api/sectors/', sector_data, name="sector_data"),
    path("sector/<str:sector_id>/", sector_view, name="sector_view"),
    path("sector/<str:sector_id>/result/<str:month>/", result_view, name="result_view"),
    path("webhook/twilio/", twilio_webhook, name="twilio_webhook"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)