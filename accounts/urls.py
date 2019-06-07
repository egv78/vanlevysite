from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from . import views

app_name = 'accounts'


urlpatterns = [
    path('', views.about, name='about'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('login_required/', LoginView.as_view(template_name='accounts/login_required.html'), name='login_required'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('profile/', views.view_profile, name='view_profile'),
    # path('profile/<int:other_user_id>/', views.view_profile_other, name='view_profile_other'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('profile/create_avatar/', views.edit_avatar, name='create_avatar'),
    path('profile/delete_avatar/<int:avatar_id>', views.edit_avatar, name='delete_avatar'),
    path('profile/edit_avatar/<int:avatar_id>', views.edit_avatar, name='edit_avatar'),

    path('profile/view_avatar/<int:avatar_id>', views.ViewAvatar.as_view()
         , name='view_avatar'),

    path('profile/pdf_charsheets/', views.ViewPDFChars.as_view(), name='pdf_charsheets'),

    path('profile/password/', views.change_password, name='password'),
    path('profile/password/success/', views.change_password_success, name='password_success'),

    path('password-reset/',
         PasswordResetView.as_view(template_name='accounts/password_reset.html',
                                   success_url='done/',
                                   email_template_name='accounts/password_reset_email.html'
                                   ),
         name='password_reset'
         ),

    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'
         ),

    path('password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(success_url='../../../complete/',
                                          template_name='accounts/password_reset_confirm.html',
                                          ),
         name='password_reset_confirm'
         ),

    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'
         )

]

