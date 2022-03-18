from django import forms

from integrated_messaging.models import Message


class MessageSendForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ("message_content", )
