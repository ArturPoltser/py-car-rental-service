from django.urls import path

from rentals.views import (
    index,
    InsuranceListView,
    InsuranceCreateView,
    InsuranceUpdateView,
    InsuranceDeleteView,
    CarListView,
    CarCreateView,
    CarDetailView,
    CarUpdateView,
    CarDeleteView,
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
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
]

app_name = "rentals"
