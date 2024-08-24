from django.urls import path
from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
]
# Removing the unnecessary comment
