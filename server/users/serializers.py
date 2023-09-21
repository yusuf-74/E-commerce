from rest_framework import serializers
from .models import User , Address , OneTimePassCode




class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email' ,'username', 'password','repeat_password','role',]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        repeat_password = data.pop('repeat_password')
        if password != repeat_password:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['flat', 'block', 'street', 'district', 'state', 'city', 'zipcode', 'country', 'is_default']

class OneTimePassCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneTimePassCode
        fields = ['user','otp', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True}            
                        }
        