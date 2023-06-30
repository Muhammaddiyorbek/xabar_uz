from django.urls import path
from django.contrib.auth.views import *
from .views import *
from django.urls import reverse_lazy

urlpatterns=[
    # path('login/',user_login,name='login')
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('password-change/',PasswordChangeView.as_view(success_url=reverse_lazy('password_change_done')),name='password_change'),
    path('password-change-done/',PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password-reset/',PasswordResetView.as_view(success_url=reverse_lazy('password_reset_done')),name='password_reset'),
    path('password-reset-done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(success_url=reverse_lazy('password_reset_complate')),name='password_reset_confirm'),
    path('password-reset/complate/',PasswordResetCompleteView.as_view(),name='password_reset_complate'),
    path('signup/',user_regster_view,name='user_regstr'),
    path('profile/',dashboard_view,name='user_profile'),
    path('profile/edit/',EditUserView.as_view(),name='edit_user_information')
]