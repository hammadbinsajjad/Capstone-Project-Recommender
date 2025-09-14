from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .ai_agent import GeminiTestingAgent
from .constants import QUERY_PREVIEW_LENGTH
from .models import Chat
from .serializers import ChatSerializer
from .utils import chat_title


class ChatsViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    ai_agent = GeminiTestingAgent()

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        ai_answer = self.ai_agent.generate_response(
            user_query=request.data.get("user_query", ""),
            chat_id=response.data["id"]
        )

        return Response({"chat": response.data, "ai_response": ai_answer})

    def perform_create(self, serializer):
        user_query = serializer.validated_data.get("user_query", "")
        serializer.save(
            user=self.request.user,
            title=chat_title(user_query),
            query_preview=user_query[:QUERY_PREVIEW_LENGTH],
        )

    def retrieve(self, request, *args, **kwargs):
        chat = self.get_object()

        if chat.user != request.user:
            return Response({"detail": "Not found."}, status=404)

        return Response({
            "chat": ChatSerializer(chat).data,
            "messages": self.ai_agent.chat_messages(chat.id),
        })

    def update(self, request, *args, **kwargs):
        chat = self.get_object()

        if chat.user != request.user:
            return Response({"detail": "Not found."}, status=404)

        response = super().update(request, *args, **kwargs)
        ai_answer = self.ai_agent.generate_response(
            user_query=request.data.get("user_query", ""),
            chat_id=chat.id,
        )

        return Response({"chat": response.data, "ai_response": ai_answer})

    def perform_update(self, serializer):
        return serializer.save(message_count=self.get_object().message_count + 2)
