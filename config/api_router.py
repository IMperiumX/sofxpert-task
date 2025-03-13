from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ticket_system.core.api.views import AgentViewSet
from ticket_system.core.api.views import TicketViewSet
from ticket_system.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("tickets", TicketViewSet)
router.register("agents", AgentViewSet)


app_name = "api"
urlpatterns = router.urls
