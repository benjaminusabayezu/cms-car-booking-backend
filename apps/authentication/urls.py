from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterView, CustomTokenObtainPairView,ForgotPasswordView,ChangePasswordView,ResetPasswordView,UserListView, UserRoleUpdateView,UserProfileView, UserSettingsView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name ='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/',ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordView.as_view(),name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

    #managing users urls
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/role/',UserRoleUpdateView.as_view(), name ='user_role_update'),

    #settings and profile
    path('profile/',UserProfileView.as_view(), name ='user_profile'),
    path('settings/', UserSettingsView.as_view(), name ='user_settings'),
]
