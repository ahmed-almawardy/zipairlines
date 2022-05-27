from unicodedata import name
from django.test import TestCase
from airplane.models import Airplane, AirplaneType
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient


data = {'type': '1', 'name': 'airplan1'}

def create_type(name='f18'):
    return AirplaneType.objects.create(name=name,)

def create_airplane():
    return Airplane.objects.create(**data)

class TestAirplane(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.type = create_type()
        cls.client = APIClient()

    def test_create_airplane(self):
        response = self.client.post(data=data, path=reverse('airplane:api-viewset-list'))
        self.assertEqual(response.status_code, HTTP_201_CREATED)
    
    def test_put_airplane(self):
        data.update(type=self.type)
        create_airplane()
        data = {'type': create_type('f16'),'name': 'airplane2'}
        response = self.client.put(data=data, path=reverse('airplane:api-viewset-detail'), args=[1])
        self.assertEqual(response.status_code, HTTP_200_OK)
        
    def test_patch_airplane(self):
        data.update(type=self.type)
        create_airplane()
        data = {'type': create_type('f16'),}
        response = self.client.patch(data=data, path=reverse('airplane:api-viewset-detail'), args=[1])
        self.assertEqual(response.status_code, HTTP_200_OK)
        
    
    def test_delete_airplane(self):
        data.update(type=self.type)
        create_airplane()
        response = self.client.delete(data=data, path=reverse('airplane:api-viewset-detail'), args=[1])
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        