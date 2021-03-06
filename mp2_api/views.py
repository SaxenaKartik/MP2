from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from mp2_api import models
from mp2_api import serializers

# Create your views here.

class HelloAPIView(APIView):
    """ Test API View """

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """ Returns a list of APIView features """
        an_apiview = ['Uses HTTP methods as function (get, post, patch, put, delete)',
        'Is similar to a traditional Django View',
        'Gives you the most control over your application logic',
        'Is mapped manually to URLs',
        ]
        return Response({'message' : 'Hello!', 'an_apiview' : an_apiview})

    def post(self, request, format=None):
        """ Create a hello message with the name"""

        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
    def put(self, request, pk = None):
        """ Handling updating an object """
        return Response({'method' : 'PUT'})

    def patch(self, request, pk = None):
        """ Handling partially updating an object """
        return Response({'method' : 'PATCH'})

    def delete(self, request, pk = None):
        """ Handling deleting an object """
        return Response({'method' : 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """ Test API View Set"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """ Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using routers',
            'Provides more functionality with less code',

        ]

        return Response({'message':'Hello!', 'a_viewset' : a_viewset})

    def create(self, request):
        """ Create a new hello message """
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'

            return Response({'message' : message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk = None):
        """ Handling updating an object """
        return Response({'http_method': 'GET'})

    def update(self, request, pk = None):
        """ Handling updating an object """
        return Response({'http_method' : 'PUT'})

    def partial_update(self, request, pk = None):
        """ Handling partially updating an object """
        return Response({'http_method' : 'PATCH'})

    def destroy(self, request, pk = None):
        """ Handling deleting an object """
        return Response({'http_method' : 'DELETE'})

# API needed for
#  - list all registered drones -> GET
#  - register new drone -> POST
#  - view specific drone using the ID -> GET (id)
#  - update the drone -> PATCH (registered_date, lat, log, battery_level, last_accessed, users_connected, status, warning_bit)
#  - delete a registered drone -> DELETE (drone_id)

# API needed for
#  - list all connected clients -> GET
#  - list clients connected to a specific drone -> GET(drone_id)
#  - list specific client -> GET(client_id)
#  - register a new client -> POST
#  - delete a client -> DELETE (client_id)

class DroneViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating drones"""

    serializer_class = serializers.DroneSerializer
    queryset = models.Drone.objects.all()


class ClientViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating drones"""

    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()
