from rest_framework import serializers
from django.contrib.auth.models import User
from todos.models import Tasks


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = [
            'user_id',
            'task_name',
            'task_description'
            # 'task_priority',
            # 'task_status'
        ]

    """def _user(self, obj):
        request = getattr(self.context, 'request', None)
        if request:
            return request.user"""