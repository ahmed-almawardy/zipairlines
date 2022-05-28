from typing import List, Dict
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.utils.translation import gettext as _
from airplane.models import Airplane
from drf_yasg import openapi

        
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
    class Meta:
        """for swagger docs """
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "airplanes",
            "properties": {
                "id": openapi.Schema(
                    title="id",
                    type=openapi.TYPE_INTEGER,
                ),
                "passengers": openapi.Schema(
                    title="passengers",
                    type=openapi.TYPE_INTEGER,
                ),
            },
            "required": ["subject", "body"],
         }

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


class AirplanesCreateSerializer(serializers.Serializer):
    """
        Write to airplanes {create, update}
        maximum 10 airplanes
        for example : {
            'airplanes': [
            {"id":1, "passengers":3},
            {"id":3, "passengers":3},
            {"id":4, "passengers":3},
            {"id":5, "passengers":3},
        ] }
    """
    airplanes:"List[Dict]" = AirplanesField(initial={'airplanes':[{"id":1, "passengers":3},{"id":2, "passengers":33}]})
    
    def create(self, validated_data) -> 'List[Dict]':
        """
            Creating the new airplanes, then get it
        """
        airplanes = Airplane.objects.bulk_create(validated_data['airplanes'])
        return AirplaneReadOnlySerializer(airplanes, many=True).data



class AirplanesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'passengers')
        model = Airplane
        extra_kwargs = {
            'id': {'read_only':True},
            'passengers': {'min_value':1},
        }
        
        def create(self, validated_data):
            raise NotImplemented('use AirplanesCreateSerializer for creating')
        
        def update(self, instance, validated_data) -> 'List[Dict]':
            """
                Only passengers are allowed to be updated, id is not allowed
            """
            instance.passengers = validated_data.get('passengers')
            instance.save()
            return AirplaneReadOnlySerializer(instance).data
