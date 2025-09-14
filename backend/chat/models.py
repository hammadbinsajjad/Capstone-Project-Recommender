from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    title = models.CharField(max_length=256, blank=False)
    query_preview = models.CharField(max_length=512, blank=True, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    message_count = models.IntegerField(default=1)
