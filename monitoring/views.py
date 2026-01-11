from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RoadSegment, SpeedReading
from .serializers import RoadSegmentSerializer, SpeedReadingSerializer
from .permissions import IsAdminOrReadOnly


class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RoadSegment model.

    Provides:
    - list: GET /api/road-segments/
    - create: POST /api/road-segments/
    - retrieve: GET /api/road-segments/{id}/
    - update: PUT /api/road-segments/{id}/
    - partial_update: PATCH /api/road-segments/{id}/
    - destroy: DELETE /api/road-segments/{id}/
    """

    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}


class SpeedReadingViewSet(viewsets.ModelViewSet):
    """ViewSet for SpeedReading model.

    Provides:
    - list: GET /api/speed-readings/
    - create: POST /api/speed-readings/
    - retrieve: GET /api/speed-readings/{id}/
    - update: PUT /api/speed-readings/{id}/
    - partial_update: PATCH /api/speed-readings/{id}/
    - destroy: DELETE /api/speed-readings/{id}/
    """

    queryset = SpeedReading.objects.select_related("road_segment").all()
    serializer_class = SpeedReadingSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Optionally filter by road_segment if query parameter is provided.
        Example: /api/speed-readings/?road_segment=1
        """
        queryset = SpeedReading.objects.select_related("road_segment").all()
        road_segment_id = self.request.query_params.get("road_segment", None)

        if road_segment_id is not None:
            queryset = queryset.filter(road_segment_id=road_segment_id)

        return queryset

    def get_serializer_context(self):
        return {"request": self.request}
