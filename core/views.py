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


def chat_list(request):
    if request.user.is_anonymous:
        return redirect('home:home')
    chats = Chat.chat_sessions(request.user)
    return render(request, 'core/chats.html',
            {'chats':chats})
def find_chat(request):
    if request.method == 'GET':
        receiver = get_object_or_404(User, username=request.GET['name'])
        print(receiver)
        return redirect("core:join_chat", receiver.username)
