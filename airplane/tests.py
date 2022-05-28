import json
from unicodedata import name
from django.test import TestCase
from airplane.models import Airplane
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient


create_data_api = {'airplanes': [
    {'id': '1', 'passengers': '2'},
    {'id': '2', 'passengers': '3'},
    {'id': '3', 'passengers': '4'},
    ]}

data =  {'id': '1', 'passengers': '2'}


def create_airplane():
    return Airplane.objects.create(**data)

class TestAirplane(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_airplane(self):
        response = self.client.post(data=create_data_api, path=reverse('airplane:api-viewset-list'), format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        
    def test_put_airplane(self):
        a1=create_airplane()
        _data = data.copy()
        _data['passengers'] = 213
        response = self.client.patch(
            path=reverse('airplane:api-viewset-detail', args=[a1.id]), data=_data, format='json'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()['airplanes']['passengers'], _data['passengers'])
                
    def test_patch_airplane(self):
        a1=create_airplane()
        _data = data.copy()
        _data['passengers'] = 23
        response = self.client.patch(
            path=reverse('airplane:api-viewset-detail', args=[a1.id]), data=_data, format='json'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()['airplanes']['passengers'], _data['passengers'])
        
    def test_delete_airplane(self):
        airplane = create_airplane()
        response = self.client.delete(reverse('airplane:api-viewset-detail', args=[airplane.id]))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        