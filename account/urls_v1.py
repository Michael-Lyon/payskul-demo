from django.urls import path
from . import views_v1

app_name = "account"

urlpatterns = [
    path("change-password/", views_v1.ChangePasswordView.as_view(), name="change_password"),
    path('create-user/', views_v1.create_user, name="create_user"),
    path('reset-password/', views_v1.reset_password_view, name='reset_password'),
    path('list-user/', views_v1.UserListView.as_view(), name="list_user"),
    path('list-user/<str:username>/', views_v1.UserDetailView.as_view(), name="list_user"),
    path('email-verify/', views_v1.confirm_email, name="confirm_email"),
    path('login/', views_v1.LoginView.as_view(), name='login'),
    path('get-auth-token/', views_v1.get_new_token, name='get_new_token'),
]
