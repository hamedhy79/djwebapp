from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('reg/', views.UserRegisterSer.as_view()),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>', views.UserFollowView.as_view(), name='user_Follow'),
    path('unfollow/<int:user_id>', views.UserUnfollowView.as_view(), name='user_Unfollow'),
    path('edit_user/', views.EditUserView.as_view(), name='edit_user'),
    path('api-token-auth/', auth_token.obtain_auth_token),
]
