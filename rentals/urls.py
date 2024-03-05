from django.urls import path

from rentals.views import (
    index,
    InsuranceListView,
    InsuranceCreateView,
    InsuranceUpdateView,
    InsuranceDeleteView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "insurances/",
        InsuranceListView.as_view(),
        name="insurance-list",
    ),
    path(
        "insurances/create/",
        InsuranceCreateView.as_view(),
        name="insurance-create",
    ),
    path(
        "insurances/<int:pk>/update/",
        InsuranceUpdateView.as_view(),
        name="insurance-update",
    ),
    path(
        "insurances/<int:pk>/delete/",
        InsuranceDeleteView.as_view(),
        name="insurance-delete",
    ),
]

app_name = "rentals"
