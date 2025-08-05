from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note
from django.contrib.auth import authenticate

# PUBLIC_INTERFACE
class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering users."""
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user

# PUBLIC_INTERFACE
class UserLoginSerializer(serializers.Serializer):
    """Serializer for logging in users."""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data

# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model CRUD."""
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'owner']
