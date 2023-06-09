import django


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



#app_name = 'accounts'

urlpatterns = [
    path('login/' , views.user_login , name='login'),
    path('logout/' , auth_views.LogoutView.as_view() , name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('register/',views.register,name='register'),
    path('verify/',views.verify_register,name='verify'),
    path('resend/' , views.resend_sms , name='resend'),
    path('follow/',views.follow ,name='follow'),
    path('<str:username>/' , views.dashboard , name='profile'),
]
