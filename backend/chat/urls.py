from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChatsViewSet


router = DefaultRouter()
router.register("chats", ChatsViewSet, basename="chats")


urlpatterns = [
    path("", include(router.urls)),
]
