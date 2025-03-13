from django.db import transaction
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ticket_system.core.api.permissions import IsAgent
from ticket_system.core.models import Ticket
from ticket_system.users.models import Agent
from ticket_system.users.models import User

from .serializers import AgentSerializer
from .serializers import TicketSellSerializer
from .serializers import TicketSerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAgent | permissions.IsAdminUser]

    def perform_create(self, serializer):
        user_data = self.request.data.pop("user")
        user = User.objects.create_user(**user_data)
        serializer.save(user=user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAgent | permissions.IsAdminUser]

    def get_queryset(self):
        """
        Optionally restricts the returned tickets to a given agent,
        by filtering against a `agent_id` query parameter in the URL.
        Admins can see all tickets.
        """
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset  # Admins see all
        if hasattr(self.request.user, "agent"):
            # Agents see only their assigned tickets
            return queryset.filter(assigned_agent=self.request.user.agent)
        return queryset.none()  # if not admin or agent return empty list

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAgent | permissions.IsAdminUser],
    )
    def fetch_tickets(self, request):
        """
        Fetches and assigns up to 15 unassigned tickets to the requesting agent.
        Uses pessimistic locking to prevent race conditions.
        """
        agent = request.user.agent
        assigned_count = agent.tickets.filter(status="assigned").count()
        tickets_to_fetch = 15 - assigned_count

        if tickets_to_fetch <= 0:
            # Agent already has 15 or more assigned tickets, return existing ones.
            existing_tickets = agent.tickets.filter(status="assigned")
            serializer = self.get_serializer(existing_tickets, many=True)
            return Response(serializer.data)

        with transaction.atomic():
            # Lock unassigned tickets to prevent other agents from claiming them.
            tickets = Ticket.objects.filter(status="unassigned").select_for_update()[
                :tickets_to_fetch
            ]

            if not tickets:
                # check if there is unassigned tickets
                return Response(
                    {"detail": "No unassigned tickets available."},
                    status=status.HTTP_200_OK,
                )

            # Assign the tickets to the agent and change their status using bulk update.
            for ticket in tickets:
                ticket.assigned_agent = agent
                ticket.status = "assigned"
                ticket.save(update_fields=["assigned_agent", "status"])

            # combine with already assigned
            all_assigned_tickets = agent.tickets.filter(Q(status="assigned"))
            serializer = self.get_serializer(all_assigned_tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAgent | permissions.IsAdminUser],
    )
    def sell_tickets(self, request):
        """
        Marks the specified tickets as 'sold' if they are assigned to the requesting agent.
        """
        try:
            agent = request.user.agent
        except Agent.DoesNotExist:
            return Response(
                {
                    "detail": f"User `{request.user}` is might be an admin but not an agent."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = TicketSellSerializer(
            data=request.data,
            many=True,
        )  # accept list of tickets.
        serializer.is_valid(raise_exception=True)

        ticket_ids = serializer.validated_data[0]["ticket_ids"]

        with transaction.atomic():
            # Lock the tickets to prevent concurrent modification
            existing_tickets = Ticket.objects.filter(
                id__in=ticket_ids,
                assigned_agent=agent,
                status="assigned",
            ).select_for_update()
            # Check if all requested tickets are assigned to the agent
            existing_ids = set(existing_tickets.values_list("pk", flat=True))
            invalid_ids = set(ticket_ids) - existing_ids
            if invalid_ids:
                return Response(
                    {
                        "detail": f"{invalid_ids} tickets are not assigned to you or do not exist or already sold.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Mark tickets as 'sold'
            for ticket in existing_tickets:
                ticket.status = "sold"
                ticket.save(update_fields=["status"])

        return Response(
            {"detail": "Tickets marked as sold."},
            status=status.HTTP_200_OK,
        )
