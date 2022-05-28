from typing import List, Dict
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.utils.translation import gettext as _
from airplane.models import Airplane

        
class AirplaneReadOnlySerializer(serializers.ModelSerializer):
    """
        Read airplanes objects from db
    """
    class Meta:
        fields = ('id', 'passengers', 'maxmium_minute_to_fly', 'total_fuel_consumption_per_minute', 'fuel_tank')
        model = Airplane
        extra_kwargs = {
            'maxmium_minute_to_fly':{'read_only':True}, 
            'total_fuel_consumption_per_minute':{'read_only':True}, 
            'fuel_tank':{'read_only':True}
        }
        

class AirplanesField(serializers.Field):
    """
        Custom DRF Field to serialize and deserialize the airplanes
    """
    
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
        if isinstance(attr_to_print, list):
            return list(map(lambda x: dict(x), attr_to_print))
        return attr_to_print
        
    def to_internal_value(self, data) -> 'List[Airplane]' :
        """
            Prepare the values to be pushed to the db rows or updated
        """
        airplanes = []
        try:
            airplanes = [Airplane(id=int(airplane.get('id')), passengers=int(airplane.get('passengers'))) \
                for airplane in data if int(airplane.get('id')) > 0 < 11 and int(airplane.get('passengers')) > 0 ]
        except ValueError:
                raise APIException(_('only integers is allowed'))
        finally:
            return airplanes


class AirplanesWriteSerializer(serializers.Serializer):
    """
        Write to airplanes {create, update}
    """
    airplanes = AirplanesField()
    passengers = serializers.IntegerField(min_value=1, allow_null=False, write_only=True, required=False)
        
    def create(self, validated_data) -> 'List[Dict]':
        """
            Creating the new airplanes, then get it
        """
        airplanes = Airplane.objects.bulk_create(validated_data['airplanes'])
        return AirplaneReadOnlySerializer(airplanes, many=True).data

    def update(self, instance, validated_data) -> 'List[Dict]':
        """
            Only passengers are allowed to be updated, id is not allowed
        """
        instance.passengers = validated_data.get('passengers')
        instance.save()
        return AirplaneReadOnlySerializer(instance).data
