from rest_framework import serializers

from ticket_system.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "username", "name", "password", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}
