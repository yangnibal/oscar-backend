from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin

from .views import RoomViewSet, MessageViewSet


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
rooms_router = router.register(r'', RoomViewSet)
rooms_router.register(
    r'messages',
    MessageViewSet,
    basename='room-messages',
    parents_query_lookups=['room']
)


urlpatterns = [
    path('', include(router.urls)),
]