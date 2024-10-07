from django.urls import path

from .views import family_diseases_create_view
from .views import family_diseases_delete_view
from .views import family_diseases_detail_view
from .views import family_diseases_list_view
from .views import family_diseases_update_view

app_name = "family-diseases"
urlpatterns = [
    path("list/<int:familiar>", view=family_diseases_list_view, name="list"),
    path("create/<int:familiar>", view=family_diseases_create_view, name="create"),
    path(
        "delete/<int:familiar>/<int:pk>/",
        view=family_diseases_delete_view,
        name="delete",
    ),
    path("edit/<int:pk>/", view=family_diseases_update_view, name="edit"),
    path("<int:pk>/", view=family_diseases_detail_view, name="detail"),
]
