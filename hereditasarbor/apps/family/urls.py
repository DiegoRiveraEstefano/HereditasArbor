from django.urls import path

from .views import familiar_create_view
from .views import familiar_delete_view
from .views import familiar_detail_view
from .views import familiar_list_view
from .views import familiar_update_view

app_name = "family"
urlpatterns = [
    path("", view=familiar_list_view, name="list"),
    path("add/", view=familiar_create_view, name="create"),
    path("delete/<int:pk>/", view=familiar_delete_view, name="remove"),
    path("edit/<int:pk>/", view=familiar_update_view, name="edit"),
    path("<int:pk>/", view=familiar_detail_view, name="detail"),
]
