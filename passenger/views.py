from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from passenger.serializers import PassengerSerializer
from passenger.models import Passenger


class PassengerAPIViewSet(ModelViewSet):
    queryset = Passenger.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PassengerSerializer
    