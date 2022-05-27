from dataclasses import fields
from email.policy import default
from passenger.models import Passenger
from rest_framework import serializers

from airplane.models import Airplane, Flight

class AirplanerSerializer(serializers.Serializer):
    passengers  = serializers.PrimaryKeyRelatedField(queryset=Passenger.objects.all(), many=True)
    id = serializers.IntegerField(max_value=10, min_value=1, default=1)

    def create(self, validated_data):
        created, airplane = Airplane.objects.get_or_create(id=validated_data['id'])
        created, flight = Flight.objects.get_or_create(airplane=airplane, is_active=True)
        flight.passengers.set(validated_data['passengers'])
        return airplane
        
class FlightSerializer(serializers.Serializer):
    airpalanes = AirplanerSerializer(many=True)
    
    def create(self, validated_data):
        print(validated_data['airpalanes'])
        return validated_data['airpalanes']



class AirplaneReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('maxmium_minute_to_fly', 'total_fuel_consumption_per_minute', 'fuel_tank')
        model = Airplane
        extra_kwargs = {
    'maxmium_minute_to_fly':{'read_only':True}, 'total_fuel_consumption_per_minute':{'read_only':True}, 'fuel_tank':{'read_only':True}
}