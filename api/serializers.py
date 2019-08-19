from rest_framework import serializers
from django.contrib.auth.models import User
from todos.models import Tasks


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name',
                  'last_name')
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "id": {"read_only": True},
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
            'id',
            'user_id',
            'title',
            'description',
            'priority',
            'status'
        ]
        extra_kwargs = {
            "description": {"required": False},
            "priority": {"required": False},
            "status": {"required": False},
            "id": {"required": False},
        }
