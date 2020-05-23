from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    """ Serializers fields for testing our APIView """
    # firstname = serializers.CharField(max_length=20)
    # lastname = serializers.CharField(max_length=20)
    # email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
    # username = serializers.CharField(max_length=20)
    # password = serializers.CharField(style={'input_type': 'password'})
    name = serializers.CharField(max_length = 20)
