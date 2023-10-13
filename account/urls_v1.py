from django.urls import path
from . import views_v1

app_name = "account"

urlpatterns = [
    path("change-password/", views_v1.ChangePasswordView.as_view(), name="change_password"),
    path('create-user/', views_v1.create_user, name="create_user"),
    path('reset-password/', views_v1.reset_password_view, name='reset_password'),
    path('security-questions/', views_v1.SecurityQuestionListAPIView.as_view(), name='security-question-list'),
    path('set-pin-questions/', views_v1.SecurityQAApiView.as_view(), name='set_pin_questions'),
    path('reset-pin-auth-code/', views_v1.reset_pin_auth_code, name='reset_pin_auth_code'),
    path('reset-pin/', views_v1.reset_pin_view, name='reset_pin'),
    path('list-user/', views_v1.UserListView.as_view(), name="list_user"),
    path('list-user/<str:username>/', views_v1.UserDetailView.as_view(), name="list_user"),
    path('email-verify/', views_v1.confirm_email, name="confirm_email"),
    path('login/', views_v1.LoginView.as_view(), name='login'),
    path('profile/', views_v1.ProfileApiView.as_view(), name='profile'),
    path('profile/update/', views_v1.ProfileUpdateView.as_view(), name='profile_update'),
    path('get-auth-token/', views_v1.get_new_token, name='get_new_token'),
]
