from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from airplane.serializers import AirplaneReadOnlySerializer, AirplanesCreateSerializer, AirplanesUpdateSerializer 
from airplane.models import Airplane


class AirplaneAPIViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    permission_classes = (AllowAny,)
    serializers = {
            'list': AirplaneReadOnlySerializer,
            'retrieve': AirplaneReadOnlySerializer,
            'update': AirplanesUpdateSerializer,
            'partial_update': AirplanesUpdateSerializer,
            'create': AirplanesCreateSerializer,
        }
        
    def get_serializer_class(self, *args, **kwargs):
        return self.serializers[self.action]        