from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from decimal import Decimal

from .models import RoadSegment, SpeedReading


class RoadSegmentViewSetTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            password="testpass123",
            is_staff=True,
        )
        self.road_segment_data = {
            "start_longitude": Decimal("103.9460064"),
            "start_latitude": Decimal("30.75066046"),
            "end_longitude": Decimal("103.9564943"),
            "end_latitude": Decimal("30.7450801"),
            "length": Decimal("1179.21"),
        }
        self.road_segment = RoadSegment.objects.create(**self.road_segment_data)

    def test_list_road_segments(self):
        url = "/api/road-segments/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("total_readings", response.data[0])

    def test_retrieve_road_segment(self):
        url = f"/api/road-segments/{self.road_segment.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.road_segment.id)
        self.assertIn("total_readings", response.data)

    def test_create_road_segment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = "/api/road-segments/"
        data = {
            "start_longitude": "104.0",
            "start_latitude": "30.7",
            "end_longitude": "104.1",
            "end_latitude": "30.8",
            "length": "1500.50",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoadSegment.objects.count(), 2)
        self.assertEqual(response.data["length"], "1500.50")

    def test_update_road_segment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = f"/api/road-segments/{self.road_segment.id}/"
        data = {
            "start_longitude": "104.0",
            "start_latitude": "30.7",
            "end_longitude": "104.1",
            "end_latitude": "30.8",
            "length": "2000.00",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.road_segment.refresh_from_db()
        self.assertEqual(self.road_segment.length, Decimal("2000.00"))

    def test_partial_update_road_segment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = f"/api/road-segments/{self.road_segment.id}/"
        data = {"length": "2500.00"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.road_segment.refresh_from_db()
        self.assertEqual(self.road_segment.length, Decimal("2500.00"))

    def test_delete_road_segment_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = f"/api/road-segments/{self.road_segment.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RoadSegment.objects.count(), 0)


class SpeedReadingViewSetTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            password="testpass123",
            is_staff=True,
        )
        self.road_segment = RoadSegment.objects.create(
            start_longitude=Decimal("103.9460064"),
            start_latitude=Decimal("30.75066046"),
            end_longitude=Decimal("103.9564943"),
            end_latitude=Decimal("30.7450801"),
            length=Decimal("1179.21"),
        )
        self.timestamp = timezone.now()
        self.speed_reading = SpeedReading.objects.create(
            road_segment=self.road_segment,
            average_speed=Decimal("31.77"),
            timestamp=self.timestamp,
        )

    def test_list_speed_readings(self):
        url = "/api/speed-readings/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("traffic_intensity", response.data[0])

    def test_retrieve_speed_reading(self):
        url = f"/api/speed-readings/{self.speed_reading.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.speed_reading.id)
        self.assertIn("traffic_intensity", response.data)

    def test_filter_by_road_segment(self):
        road_segment2 = RoadSegment.objects.create(
            start_longitude=Decimal("104.0"),
            start_latitude=Decimal("30.7"),
            end_longitude=Decimal("104.1"),
            end_latitude=Decimal("30.8"),
            length=Decimal("1500.50"),
        )
        SpeedReading.objects.create(
            road_segment=road_segment2,
            average_speed=Decimal("45.00"),
            timestamp=timezone.now(),
        )

        url = f"/api/speed-readings/?road_segment={self.road_segment.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["road_segment"], self.road_segment.id)

    def test_create_speed_reading_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = "/api/speed-readings/"
        data = {
            "road_segment": self.road_segment.id,
            "average_speed": "25.50",
            "timestamp": timezone.now().isoformat(),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpeedReading.objects.count(), 2)
        self.assertEqual(response.data["average_speed"], "25.50")

    def test_traffic_intensity_calculation_elevada(self):
        reading = SpeedReading.objects.create(
            road_segment=self.road_segment,
            average_speed=Decimal("18.50"),
            timestamp=timezone.now(),
        )
        self.assertEqual(reading.traffic_intensity, "elevada")

    def test_traffic_intensity_calculation_media(self):
        reading = SpeedReading.objects.create(
            road_segment=self.road_segment,
            average_speed=Decimal("35.00"),
            timestamp=timezone.now(),
        )
        self.assertEqual(reading.traffic_intensity, "média")

    def test_traffic_intensity_calculation_baixa(self):
        reading = SpeedReading.objects.create(
            road_segment=self.road_segment,
            average_speed=Decimal("65.00"),
            timestamp=timezone.now(),
        )
        self.assertEqual(reading.traffic_intensity, "baixa")

    def test_traffic_intensity_in_api_response(self):
        url = f"/api/speed-readings/{self.speed_reading.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("traffic_intensity", response.data)
        self.assertIn(response.data["traffic_intensity"], ["elevada", "média", "baixa"])


class PermissionTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            password="testpass123",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="regular",
            password="testpass123",
            is_staff=False,
        )
        self.road_segment = RoadSegment.objects.create(
            start_longitude=Decimal("103.9460064"),
            start_latitude=Decimal("30.75066046"),
            end_longitude=Decimal("103.9564943"),
            end_latitude=Decimal("30.7450801"),
            length=Decimal("1179.21"),
        )
        self.speed_reading = SpeedReading.objects.create(
            road_segment=self.road_segment,
            average_speed=Decimal("31.77"),
            timestamp=timezone.now(),
        )

    def test_anonymous_can_read_road_segments(self):
        url = "/api/road-segments/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_read_specific_road_segment(self):
        url = f"/api/road-segments/{self.road_segment.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_road_segment(self):
        url = "/api/road-segments/"
        data = {
            "start_longitude": "104.0",
            "start_latitude": "30.7",
            "end_longitude": "104.1",
            "end_latitude": "30.8",
            "length": "1500.50",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_update_road_segment(self):
        url = f"/api/road-segments/{self.road_segment.id}/"
        data = {"length": "2000.00"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_delete_road_segment(self):
        url = f"/api/road-segments/{self.road_segment.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_can_read_speed_readings(self):
        url = "/api/speed-readings/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_speed_reading(self):
        url = "/api/speed-readings/"
        data = {
            "road_segment": self.road_segment.id,
            "average_speed": "25.50",
            "timestamp": timezone.now().isoformat(),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_create_road_segment(self):
        self.client.force_authenticate(user=self.regular_user)
        url = "/api/road-segments/"
        data = {
            "start_longitude": "104.0",
            "start_latitude": "30.7",
            "end_longitude": "104.1",
            "end_latitude": "30.8",
            "length": "1500.50",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_road_segment(self):
        self.client.force_authenticate(user=self.admin_user)
        url = "/api/road-segments/"
        data = {
            "start_longitude": "104.0",
            "start_latitude": "30.7",
            "end_longitude": "104.1",
            "end_latitude": "30.8",
            "length": "1500.50",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update_road_segment(self):
        self.client.force_authenticate(user=self.admin_user)
        url = f"/api/road-segments/{self.road_segment.id}/"
        data = {"length": "2000.00"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_road_segment(self):
        self.client.force_authenticate(user=self.admin_user)
        url = f"/api/road-segments/{self.road_segment.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_create_speed_reading(self):
        self.client.force_authenticate(user=self.admin_user)
        url = "/api/speed-readings/"
        data = {
            "road_segment": self.road_segment.id,
            "average_speed": "25.50",
            "timestamp": timezone.now().isoformat(),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
