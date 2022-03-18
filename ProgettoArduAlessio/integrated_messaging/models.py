from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from user_management.models import MyUser


class Message(models.Model):
    sender = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name="sender_messages")
    receiver = models.ForeignKey(MyUser, on_delete=models.PROTECT, related_name="receiver_messages")
    message_content = models.CharField(max_length=140)
    date = models.DateTimeField(auto_now=True)
