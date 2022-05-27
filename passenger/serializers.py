from rest_framework.serializers import ModelSerializer
from passenger.models import Passenger


class PassengerSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Passenger
        depth = 2
        extra_kwargs = {
            'id': {'read_only': True},
            'flights': {'read_only': True},
        }