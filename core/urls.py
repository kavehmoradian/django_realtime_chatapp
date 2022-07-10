from django.urls import path
from .views import join_chat

app_name = 'core'

urlpatterns = [
    path('<str:receiver>/', join_chat, name='join_chat'),
]
