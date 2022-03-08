import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect

from integrated_messaging.forms import MessageSendForm
from integrated_messaging.models import Message
from user_management.models import MyUser


@login_required
def inbox_home(request):
    # selecting distinct senders
    list_of_dict_received = request.user.receiver_messages.values('sender').distinct()
    list_of_dict_sent = request.user.sender_messages.values('receiver').distinct()
    pk_senders = []
    pk_receivers = []
    for dic in list_of_dict_received:
        pk_senders.append(dic['sender'])
    for dic in list_of_dict_sent:
        pk_receivers.append(dic['receiver'])

    senders = MyUser.objects.filter(pk__in=pk_senders)
    receivers = MyUser.objects.filter(pk__in=pk_receivers)

    chat_users = senders.union(receivers)
    chat_user_count = chat_users.count()

    chat_user_dict = {}
    for chat_user in chat_users:
        messages1 = Message.objects.filter(sender=chat_user, receiver=request.user.pk)
        messages2 = Message.objects.filter(sender=request.user.pk, receiver=chat_user)
        chat_user_dict[chat_user] = messages1.union(messages2).order_by("-date").first()

    context = {
        "chat_users": chat_user_dict,
        "chat_user_count": chat_user_count,
    }
    return render(request, "integrated_messaging/inbox_home.html", context)


@login_required
def send_message(request, pk_receiver=""):
    receiver = MyUser.objects.get(pk=pk_receiver)
    if request.POST:
        form = MessageSendForm(request.POST)
        if form.is_valid():
            message = Message(sender=MyUser.objects.get(pk=request.user.pk), receiver=receiver,
                              message_content=form.cleaned_data['message_content'])
            message.save()
            return redirect(reverse_lazy("user_management:home", args=(receiver.pk,)))
    else:
        form = MessageSendForm()
        return render(request, "integrated_messaging/message/send.html", {
            "receiver": receiver,
            "form": form,
            "url": reverse_lazy("user_management:home", args=(receiver.pk,))
        })


@csrf_protect
def send_message_inline_ajax(request):

    if request.POST:
        message_content = request.POST.get('message_content')
        receiver = MyUser.objects.get(pk=request.POST.get('receiver_pk'))
        message = Message(sender=MyUser.objects.get(pk=request.user.pk), receiver=receiver,
                          message_content=message_content)
        message.save()

        #response_data = {'html_message': render(request, "integrated_messaging/message/my_message.html", {"message": message})}
        # return HttpResponse(
        #     json.dumps(response_data),
        #     content_type="application/json"
        # )
        return render(request, "integrated_messaging/message/my_message.html", {"message": message})
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required
def message_list(request, pk_sender=""):
    sender = MyUser.objects.get(pk=pk_sender)
    messages1 = Message.objects.filter(sender=sender, receiver=request.user.pk)
    messages2 = Message.objects.filter(sender=request.user.pk, receiver=sender)
    messages = messages1.union(messages2).order_by("date")

    return render(request, "integrated_messaging/message/list.html", {"messages": messages, "sender_view": sender})