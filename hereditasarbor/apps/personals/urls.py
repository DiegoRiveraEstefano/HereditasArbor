from django.urls import path

from .views import personal_data_create_view
from .views import personal_data_detail_view
from .views import personal_data_time_stamp_data_create_view
from .views import personal_data_time_stamp_data_delete_view
from .views import personal_data_time_stamp_data_detail_view
from .views import personal_data_time_stamp_data_list_view
from .views import personal_data_time_stamp_data_update_view
from .views import personal_data_update_view

app_name = "personal"
urlpatterns = [
    path("", view=personal_data_detail_view, name="me"),
    path("create/", view=personal_data_create_view, name="create"),
    path("update/", view=personal_data_update_view, name="update"),
    path(
        "time_stamp/",
        view=personal_data_time_stamp_data_list_view,
        name="time_stamp-list",
    ),
    path(
        "time_stamp/<int:pk>",
        view=personal_data_time_stamp_data_detail_view,
        name="time_stamp-detail",
    ),
    path(
        "time_stamp/create/",
        view=personal_data_time_stamp_data_create_view,
        name="time_stamp-create",
    ),
    path(
        "time_stamp/edit/<int:pk>",
        view=personal_data_time_stamp_data_update_view,
        name="time_stamp-edit",
    ),
    path(
        "time_stamp/delete/<int:pk>",
        view=personal_data_time_stamp_data_delete_view,
        name="time_stamp-delete",
    ),
]
