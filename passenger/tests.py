from django.test import TestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient
from passenger.models import Passenger


data = {
            'name': 'ahmed',
            'email': 'ahmed@me.com',
            'phone': '0123456987',
        }

def create_passenger():
    return Passenger.objects.create(**data)
    
class TestPassenger(TestCase):
    """
       TEST for a Passenger in an airplane
    """
    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_create_passenger(self):
        
        response = self.client.post(reverse('passenger:api-viewset-list'), data=data)
        
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        
    def test_patch_passenger(self):
        create_passenger()
        data = {
            'email': 'Ahmed@me.com',
        }
        response = self.client.patch(reverse('passenger:api-viewset-detail', args=[1]), data=data)
        
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_put_passenger(self):
        create_passenger()
        data = {
            'name': 'AhmeD',
            'email': 'Ahmed@me.com',
            'phone': '22222222',
        }
        response = self.client.put(reverse('passenger:api-viewset-detail', args=[1]), data=data)
        
        self.assertEqual(response.status_code, HTTP_200_OK)


    def test_delete_passenger(self):
        create_passenger()
        response = self.client.delete(reverse('passenger:api-viewset-detail', args=[1]))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)