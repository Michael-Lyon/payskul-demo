from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from . import views


app_name = "apiv1"


urlpatterns = [
    path("auth/", obtain_auth_token, name="obtain_auth_token"),
    path("account/", include("account.urls_v1", namespace="account_url")),
    path("core/", include("core.urls_v1", namespace="core")),
    path("", views.home, name="home"),
]
