from pyexpat import model
from rest_framework import serializers

from airplane.models import Airplane

        
class AirplaneWriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Airplane

        
class AirplaneReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'passengers', 'maxmium_minute_to_fly', 'total_fuel_consumption_per_minute', 'fuel_tank')
        model = Airplane
        extra_kwargs = {
            'maxmium_minute_to_fly':{'read_only':True}, 
            'total_fuel_consumption_per_minute':{'read_only':True}, 
            'fuel_tank':{'read_only':True}
        }
        
        
class AirplanesWriteSerializer(serializers.Serializer):
    airplanes = AirplaneWriteSerializer(many=True, write_only=True)
    
    def create(self, validated_data):
        airplanes = [Airplane(id=airplane['id'], passengers=airplane['passengers']) for airplane in validated_data['airplanes']]
        airplanes = Airplane.objects.bulk_create(airplanes)
        return list(map(lambda x: {x.id, x.passengers}, airplanes))
     