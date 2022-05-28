from rest_framework import serializers
from airplane.models import Airplane
from typing import List, Dict

        
class AirplaneReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'passengers', 'maxmium_minute_to_fly', 'total_fuel_consumption_per_minute', 'fuel_tank')
        model = Airplane
        extra_kwargs = {
            'maxmium_minute_to_fly':{'read_only':True}, 
            'total_fuel_consumption_per_minute':{'read_only':True}, 
            'fuel_tank':{'read_only':True}
        }
        
     

class AirplanesField(serializers.Field):
    def to_representation(self, value) ->'List[Dict]' :
        """
            Serializering tjhe field back after processing it

            Ps: here i could do something, like query to db and list all the 10 airplanes
            but it is not supposed to be in create
        """
        return value 
        
    def get_attribute(self, attr_to_print) -> 'List[Dict]' :
        """
            Prepare to serilizer the field back after porcessing it     
        """
        return list(map(lambda x: dict(x), attr_to_print))
        
        
    def to_internal_value(self, data) -> 'List[Airplane]' :
        """
            Prepare the values to be pushed to the db rows
        """
        airplanes = [ Airplane(id=airplane.get('id'), passengers=airplane.get('passengers')) \
            for airplane in data if airplane.get('id') > 0 < 11 and airplane.get('passengers') > 0 ]
        return airplanes

class AirplanesWriteSerializer(serializers.Serializer):
    airplanes = AirplanesField()
    
    def create(self, validated_data) -> 'List[Dict]':
        """
            Creating the new airplanes, then get it
        """
        airplanes = Airplane.objects.bulk_create(validated_data['airplanes'])
        return AirplaneReadOnlySerializer(airplanes, many=True).data