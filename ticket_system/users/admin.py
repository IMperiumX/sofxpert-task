from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from ticket_system.core.models import Ticket

from .forms import UserAdminChangeForm
from .models import Agent
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    fields = (
        "title",
        "subject",
        "description",
        "status",
        "assigned_agent",
        "created_at",
    )
    readonly_fields = ("created_at",)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_filter = ("user",)
    inlines = [TicketInline]
