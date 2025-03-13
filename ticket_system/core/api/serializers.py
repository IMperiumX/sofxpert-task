from rest_framework import serializers

from ticket_system.core.models import Ticket
from ticket_system.users.api.serializers import UserSerializer
from ticket_system.users.models import Agent


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Agent
        fields = ["id", "user"]


class TicketSerializer(serializers.ModelSerializer):
    assigned_agent = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(),
        required=False,
        allow_null=True,
    )
    status = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "created_at",
            "assigned_agent",
            "title",
            "status",
            "description",
            "subject",
            "customer_name",
            "customer_email",
        ]
        read_only_fields = ["created_at"]


class TicketSellSerializer(serializers.Serializer):
    ticket_ids = serializers.ListField(child=serializers.IntegerField(min_value=0))
