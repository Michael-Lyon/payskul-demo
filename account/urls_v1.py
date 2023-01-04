from django.urls import path
from . import views_v1

app_name = "account"

urlpatterns = [
    path('list-create-user', views_v1.UserListCreateView.as_view(), name="list_create_user"),
    path('email-verify/', views_v1.confirm_email, name="confirm_email"),
    path('login/', views_v1.LoginView.as_view(), name='login'),
]
