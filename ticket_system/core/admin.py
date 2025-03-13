from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "assigned_agent",
        "title",
        "status",
        "description",
        "subject",
        "customer_name",
        "customer_email",
    )
    list_filter = ("created_at", "assigned_agent")
    date_hierarchy = "created_at"
    search_fields = ("description", "subject", "customer_name", "customer_email")
    ordering = ("created_at",)
