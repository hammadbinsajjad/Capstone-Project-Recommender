from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    user_query = serializers.CharField(write_only=True, required=True, allow_blank=False)
    created_date = serializers.DateTimeField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)
    message_count = serializers.IntegerField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Chat
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop("user_query", None)
        return super().create(validated_data)
