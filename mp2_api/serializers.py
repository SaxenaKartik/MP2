from rest_framework import serializers
from mp2_api import models
# from django.contrib.auth.hashers import make_password
import hashlib

def hashit(k : str):
    hash = hashlib.sha1()
    hash.update(k.encode('utf-8'))
    return  hash.hexdigest()[:-10]

class HelloSerializer(serializers.Serializer):
    """ Serializes fields for testing our APIView """
    name = serializers.CharField(max_length = 20)

class DroneSerializer(serializers.ModelSerializer):
    """Serializes fields for Drone Model"""
    class Meta :
        model = models.Drone
        fields = ('drone_id', 'registered_date', 'lat', 'log', 'battery_level', 'last_accessed', 'users_connected', 'status', 'warning_bit')
        extra_kwargs = {
            'drone_id' :{
                'style' : {'input_type' : 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new drone"""
        # drone = models.Drone(
        #     drone_id = make_password(validated_data['drone_id'])
        #     registered_date = validated_data['registered_date']
        #     lat = validated_data['lat']
        #     log = validated_data['log']
        #     battery_level = validated_data['battery_level']
        #     last_accessed = validated_data['last_accessed']
        #     users_connected = validated_data['users_connected']
        #     status = validated_data['status']
        #     warning_bit = validated_data['warning_bit']
        # )
        # drone.save()

        validated_data['drone_id'] = validated_data.get('drone_id')

        # validated_data['drone_id'] = hashit(validated_data.get('drone_id'))

        return super(DroneSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """Handle updating drone"""
        if 'drone_id' in validated_data:
            validated_data['drone_id'] = validated_data.get('drone_id')

            # validated_data['drone_id'] = hashit(validated_data.get('drone_id'))
            # instance.drone_id = hashit(validated_data.get('drone_id', instance.drone_id))
        return super(DroneSerializer, self).update(instance, validated_data)

class ClientSerializer(serializers.ModelSerializer):
    """ Serializes fields for Client Models"""
    class Meta:
        model = models.Client
        fields = (
        'client_id', 'login_time', 'logout_time', 'ip_address', 'drone_id')
        extra_kwargs = {
            'client_id' : {
                'style' : {'input_type': 'password'}
            }
        }
    def create(self, validated_data):
        """Create and return a new client"""
        validated_data['client_id'] = validated_data.get('client_id')


        # validated_data['client_id'] = hashit(validated_data.get('client_id'))
        return super(ClientSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """Handle updating client"""
        if 'client_id' in validated_data:
            validated_data['client_id'] = validated_data.get('client_id')

            # validated_data['client_id'] = hashit(validated_data.get('client_id'))
            # instance.client_id = make_password(validated_data.get('client_id', instance.client_id))
        return super(ClientSerializer, self).update(instance, validated_data)
