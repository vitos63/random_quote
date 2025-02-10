
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from users.views import LoginUser, EditProfileUserView, RegisterUser, ProfileUserSavedQuotesView, ProfileUserSuggestedQuotesView, ProfileUserDeleteSavedQuotesView

app_name= 'users'

urlpatterns = [
    path('login/',LoginUser.as_view(),  name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('register/',RegisterUser.as_view(), name='register'),
    path('profile/suggested-quotes/',ProfileUserSuggestedQuotesView.as_view(), name='suggested_quotes'),
    path('profile/saved-quotes/',ProfileUserSavedQuotesView.as_view(), name='saved_quotes'),
    path('profile/delete-saved-quotes/<int:id>/',ProfileUserDeleteSavedQuotesView.as_view(), name='delete_saved_quotes'),
    
    path('edit-profile/',EditProfileUserView.as_view(), name='edit_profile'),
    path('password-reset/',PasswordResetView.as_view(success_url = reverse_lazy('users:password_reset_done'), 
                                                     template_name = 'users/user_form.html', 
                                                     email_template_name='users/password_reset_email.html', 
                                                     extra_context ={'title':'Сброс пароля', 'button':'Выслать'}), 
                                                     name='password_reset'),
    path('password-reset/done/',PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url = reverse_lazy('password_reset_done'),
                                                                              template_name= 'users/user_form.html',
                                                                              extra_context={'button':'Сменить пароль'}),
                                                                                name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name= 'users/password_reset_complete.html'), name='password_reset_complite'),
]
