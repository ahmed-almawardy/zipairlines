from django.urls import path, include
from rest_framework.routers import DefaultRouter
from airplane.views import AirplaneAPIViewSet

app_name = 'airplane'

router = DefaultRouter()
router.register('', AirplaneAPIViewSet, basename='api-viewset')

urlpatterns = [
    path('', include(router.urls)),
]
