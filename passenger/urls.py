from django.urls import path, include
from rest_framework.routers import DefaultRouter
from passenger.views import PassengerAPIViewSet

app_name = 'passenger'

router = DefaultRouter()
router.register('', PassengerAPIViewSet, basename='api-viewset')

urlpatterns = [
    path('', include(router.urls)),
]
