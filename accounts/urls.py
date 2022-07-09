from django.urls import path
from .views import UserLoginView, UserRegistrationView, UserLogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegistrationView.as_view(), name='user_register')
]
