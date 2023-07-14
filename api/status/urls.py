from django.urls import path
from . import views

urlpatterns = [
    path("", views.StatusCreateListApi.as_view(), name="status"),
    path(
        "<int:status_id>/",
        views.StatusRetrieveUpdateDelete.as_view(),
        name="status_details",
    ),
]
