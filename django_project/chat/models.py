from django.db import models


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.IntegerField()

    class Meta:
        app_label = "chat"
