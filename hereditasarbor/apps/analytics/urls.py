from django.urls import path

from .views import analytics_create_view
from .views import analytics_detail_view
from .views import analytics_list_view

app_name = "analytics"
urlpatterns = [
    path("", view=analytics_list_view, name="analytic-list"),
    path("create/", view=analytics_create_view, name="analytic-create"),
    path("detail/<int:pk>/", view=analytics_detail_view, name="analytic-detail"),
]
