from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import *
from .serializers import PerevalSerializer


class PerevalApiTestCase(APITestCase):

    def setUp(self):
        user1 = MyUser.objects.create(email='Test1', phone=1111111111, fam='Test1', name='Test1', otc='Test1')
        user2 = MyUser.objects.create(email='Test2', phone=2222222222, fam='Test2', name='Test2', otc='Test2')
        coord1 = Coord.objects.create(latitude=323.12, longitude=323.12, height=1400)
        coord2 = Coord.objects.create(latitude=323.12, longitude=323.12, height=1400)
        level1 = Level.objects.create(winter='1a', spring='1a', summer='1a', autumn='1a')
        level2 = Level.objects.create(winter='1a', spring='1a', summer='1a', autumn='1a')
        self.pereval1 = Pereval.objects.create(user_id=user1, beauty_title='beauty_title1', title="title1",
                                               other_titles='other_titles1', coord_id=coord1, level_id=level1)
        self.pereval2 = Pereval.objects.create(user_id=user2, beauty_title='beauty_title2', title="title2",
                                               other_titles='other_titles2', coord_id=coord2, level_id=level2)

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval1, self.pereval2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.pereval1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class MountSerializerTestCase(TestCase):
    def setUp(self):
        user1 = MyUser.objects.create(email="Test1", phone=1111111111, fam="Test1", name="Test1", otc="Test1")
        user2 = MyUser.objects.create(email="Test2", phone=2222222222, fam="Test2", name="Test2", otc="Test2")
        coord1 = Coord.objects.create(latitude=323.12, longitude=323.12, height=1400)
        coord2 = Coord.objects.create(latitude=323.12, longitude=323.12, height=1400)
        level1 = Level.objects.create(winter='1a', spring='1a', summer='1a', autumn='1a')
        level2 = Level.objects.create(winter='1a', spring='1a', summer='1a', autumn='1a')
        self.pereval1 = Pereval.objects.create(user_id=user1, beauty_title="beauty_title1", title="title1",
                                               other_titles="other_titles1", coord_id=coord1, level_id=level1)
        self.pereval2 = Pereval.objects.create(user_id=user2, beauty_title="beauty_title2", title="title2",
                                               other_titles="other_titles2", coord_id=coord2, level_id=level2)

    def test_check(self):
        serializer_data = PerevalSerializer([self.pereval1, self.pereval2], many=True).data

        expected_data = [
            {
                "id": 1,
                "beauty_title": "beauty_title1",
                "title": "title1",
                "other_titles": "other_titles1",
                "connect": None,
                "add_time": self.pereval1.add_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "user_id": {
                    "email": "Test1",
                    "fam": "Test1",
                    "name": "Test1",
                    "otc": "Test1",
                    "phone": "1111111111"
                },
                "coord_id": {
                    "latitude": 323.12,
                    "longitude": 323.12,
                    "height": 1400
                },
                "level_id": {
                    "winter": "1a",
                    "summer": "1a",
                    "autumn": "1a",
                    "spring": "1a"
                },
                "images": [],
                "status": "NW"
            },
            {
                "id": 2,
                "beauty_title": "beauty_title2",
                "title": "title2",
                "other_titles": "other_titles2",
                "connect": None,
                "add_time": self.pereval2.add_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "user_id": {
                    "email": "Test2",
                    "fam": "Test2",
                    "name": "Test2",
                    "otc": "Test2",
                    "phone": "2222222222"
                },
                "coord_id": {
                    "latitude": 323.12,
                    "longitude": 323.12,
                    "height": 1400
                },
                "level_id": {
                    "winter": "1a",
                    "summer": "1a",
                    "autumn": "1a",
                    "spring": "1a"
                },
                "images": [],
                "status": "NW"
            }
        ]
        # print(expected_data)
        # print(serializer_data)
        self.assertEqual(serializer_data, expected_data)
