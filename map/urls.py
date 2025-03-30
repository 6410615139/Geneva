from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path("", map_view, name="map_view"),
    path("sector_map/<str:sector_name>/", sector_map, name="sector_map"),
    path("sector/<str:sector_name>/", sector_view, name="sector_view"),
    path("rain_fall/<str:sector_name>/", rain_view, name="rain_view"),
    path("spi_view/<str:sector_name>/", spi_view, name="spi_view"),
    path("warning_view/<str:sector_name>/", warning_view, name="warning_view"),
    path("crop_view/<str:sector_name>/", crop_view, name="crop_view"),
    path("income_view/<str:sector_name>/", income_view, name="income_view"),
    path("sector/<str:sector_name>/result/<str:month>/", result_view, name="result_view"),
    path("webhook/twilio/", twilio_webhook, name="twilio_webhook"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)