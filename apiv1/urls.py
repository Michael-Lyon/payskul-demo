from django.urls import path, include
from . import views


app_name = "apiv1"


urlpatterns = [
    path("", views.home, name="home"),
    path("account/", include("account.urls_v1", namespace="account_url")),
    path("core/", include("core.urls_v1", namespace="core_url")),
]
