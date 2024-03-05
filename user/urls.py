from django.urls import path

from user.views import (
    RenterListView,
    RenterCreateView,
    RenterDetailView,
    RenterUpdateView,
    RenterDeleteView,
)

urlpatterns = [
    path("renters/", RenterListView.as_view(), name="renter-list"),
    path("renters/create/", RenterCreateView.as_view(), name="renter-create"),
    path(
        "renters/<int:pk>/", RenterDetailView.as_view(), name="renter-detail"
    ),
    path("renters/update/", RenterUpdateView.as_view(), name="renter-update"),
    path(
        "renters/<int:pk>/delete/",
        RenterDeleteView.as_view(),
        name="renter-delete",
    ),
]

app_name = "user"
