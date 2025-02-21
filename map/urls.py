from django.urls import path
from .views import *

urlpatterns = [
    path("", map_view, name="map_view"),
    path('api/sectors/', sector_data, name="sector_data"),
    path("sector/<str:sector_id>/", sector_view, name="sector_view"),
    path("sector/<str:sector_id>/result/<str:month>/", result_view, name="result_view"),
]
