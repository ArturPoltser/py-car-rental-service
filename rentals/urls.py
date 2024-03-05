from django.urls import path

from rentals.views import index


urlpatterns = [
    path("", index, name="index"),
]

app_name = "rentals"
