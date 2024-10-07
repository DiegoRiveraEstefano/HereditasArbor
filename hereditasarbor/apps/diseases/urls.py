from django.urls import path

from .views import disease_detail_view

app_name = "diseases"
urlpatterns = [
    path("<int:pk>/", view=disease_detail_view, name="detail"),
]
