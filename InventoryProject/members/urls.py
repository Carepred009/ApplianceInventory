from django.urls import path

from .views import SignUpView, UserDetailView, UserProfileView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),

    path('user_profile/', UserDetailView.as_view(), name="user_profile"),

    path('create_profile/', UserProfileView.as_view(), name="create_profile"),
]