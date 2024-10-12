from django.urls import path

from .views import user_create_view
from .views import user_detail_view
from .views import user_log_out_view
from .views import user_login_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("redirect/", view=user_redirect_view, name="redirect"),
    path("update/", view=user_update_view, name="update"),
    path("create/", view=user_create_view, name="create"),
    path("login/", view=user_login_view, name="login"),
    path("logout/", view=user_log_out_view, name="logout"),
    path("me/", view=user_detail_view, name="me"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
