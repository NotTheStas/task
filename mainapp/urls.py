from django.urls import path
from .views import *

urlpatterns = [
    path('', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile_user, name='profile'),
    path('profile/change-password/', change_password_user, name='change_password'),
    path('profile/change-username/', change_username_user, name='change_username'),
    path('profile/delete-account/', delete_account_user, name='delete_account'),
]