from django.urls import path
from .views import join_chat, chat_list, find_chat

app_name = 'core'

urlpatterns = [
    path('find/', find_chat, name='find_chat'),
    path('', chat_list, name='chat_list' ),
    path('<str:receiver>/', join_chat, name='join_chat'),
]
