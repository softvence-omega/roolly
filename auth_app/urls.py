from django.urls import path
from . import views
from django.contrib.auth import views as django_auth_views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('update/', views.UpdateUserAPIView.as_view(), name='update-user'),
    path('send-otp/', views.SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('password_reset/', django_auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', django_auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', django_auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),
]
