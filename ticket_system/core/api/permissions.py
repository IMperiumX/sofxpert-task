from rest_framework import permissions


class IsAgent(permissions.BasePermission):
    """
    Custom permission to only allow agents to access the object.
    """

    def has_permission(self, request, view):
        # Allow all users to access the list view
        if view.action == "list":
            return True
        return request.user and hasattr(request.user, "agent")

    def has_object_permission(self, request, view, obj):
        from ticket_system.users.models import Agent

        # Agents can only access their own agent instance
        if isinstance(obj, Agent):
            return obj.user == request.user

        return False
