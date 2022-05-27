from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from airplane.serializers import FlightSerializer, AirplaneReadOnlySerializer
from airplane.models import Airplane


class AirplaneAPIViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = FlightSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['list', 'retrieve']:
            return AirplaneReadOnlySerializer
        else:
            return FlightSerializer