from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from airplane.serializers import AirplaneReadOnlySerializer, AirplanesWriteSerializer
from airplane.models import Airplane


class AirplaneAPIViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['list', 'retrieve']:
            return AirplaneReadOnlySerializer
        else:
            return AirplanesWriteSerializer