from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Chat, Message
from accounts.models import User

def join_chat(request, receiver):
    if request.user.is_anonymous:
        return redirect('home:home')
    user1 = request.user
    user2 = get_object_or_404(User, username=receiver)
    Chat.create_if_not_exists(user1, user2)
    chat_session = Chat.chat_session_exists(user1,user2)
    messages = Message.objects.filter(chat=chat_session).all()

    return render(request, 'core/joinchat.html',
            {'receiver': receiver, 'messages': messages})
