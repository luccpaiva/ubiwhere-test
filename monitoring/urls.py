from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoadSegmentViewSet, SpeedReadingViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r"road-segments", RoadSegmentViewSet, basename="road-segment")
router.register(r"speed-readings", SpeedReadingViewSet, basename="speed-reading")

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
]
