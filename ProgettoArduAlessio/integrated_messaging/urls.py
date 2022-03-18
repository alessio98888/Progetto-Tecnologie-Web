from integrated_messaging import views
from django.urls import path

app_name = "integrated_messaging"

urlpatterns = [
    path("send/<int:pk_receiver>", views.send_message, name="message-send"),
    path("inbox/", views.inbox_home, name="inbox"),
    path("inbox/message/list/<int:pk_sender>", views.message_list, name="message-list"),
    path("inbox/send_message_inline_ajax", views.send_message_inline_ajax, name="send-message-inline-ajax"),
]