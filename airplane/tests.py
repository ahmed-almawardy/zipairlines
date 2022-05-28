from unicodedata import name
from django.test import TestCase
from airplane.models import Airplane
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient


data = {'airplanes': [{'id': '1', 'passengers': '2'}]}

def create_airplane():
    return Airplane.objects.create(**data)

class TestAirplane(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_airplane(self):
        response = self.client.post(data=data, path=reverse('airplane:api-viewset-list'), format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
    
    def test_put_airplane(self):
        create_airplane()
        response = self.client.put(data={'id':3, 'passengers':5}, path=reverse('airplane:api-viewset-detail'), args=[1])
        self.assertEqual(response.status_code, HTTP_200_OK)
        
    def test_patch_airplane(self):
        create_airplane()
        response = self.client.patch(data={'passengers':4}, path=reverse('airplane:api-viewset-detail'), args=[1])
        self.assertEqual(response.status_code, HTTP_200_OK)
        
    
    def test_delete_airplane(self):
        create_airplane()
        response = self.client.delete(data=data, path=reverse('airplane:api-viewset-detail'), args=[1])
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        