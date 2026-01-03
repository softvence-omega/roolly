from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            Profile.objects.create(user=user, phone=profile_data.get('phone'))
        else:
            Profile.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError("Either email or phone must be provided.")
        return data

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError("Either email or phone must be provided.")
        return data

class UpdateUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', required=False)
    image = serializers.ImageField(source='profile.image', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'image']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        if profile_data:
            profile = instance.profile
            profile.phone = profile_data.get('phone', profile.phone)
            profile.image = profile_data.get('image', profile.image)
            profile.save()
        
        return instance
