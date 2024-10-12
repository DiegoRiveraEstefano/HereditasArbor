from django.urls import path

from .views import analytics_detail_view
from .views import analytics_index_view

app_name = "analytics"
urlpatterns = [
    path("", view=analytics_index_view, name="index"),
    path("detail/<int:pk>/", view=analytics_detail_view, name="detail"),
]
