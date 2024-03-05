from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from rentals.models import Car, Insurance, Rental


def index(request: HttpRequest) -> HttpResponse:
    num_renters = get_user_model().objects.count()
    num_cars = Car.objects.count()
    num_insurances = Insurance.objects.count()

    context = {
        "num_renters": num_renters,
        "num_cars": num_cars,
        "num_insurances": num_insurances,
    }

    return render(request, "rentals/index.html", context=context)


class InsuranceListView(LoginRequiredMixin, generic.ListView):
    model = Insurance
    paginate_by = 5


class InsuranceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Insurance
    fields = "__all__"
    success_url = reverse_lazy("rentals:insurance-list")


class InsuranceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Insurance
    fields = "__all__"
    success_url = reverse_lazy("rentals:insurance-list")


class InsuranceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Insurance
    success_url = reverse_lazy("rentals:insurance-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("rentals:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("rentals:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("rentals:car-list")


class RentalListView(LoginRequiredMixin, generic.ListView):
    queryset = Rental.objects.select_related("car")
    paginate_by = 5


class RentalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Rental
    fields = "__all__"
    success_url = reverse_lazy("rentals:rental-list")


class RentalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Rental


class RentalUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Rental
    fields = "__all__"
    success_url = reverse_lazy("rentals:rental-list")


class RentalDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Rental
    success_url = reverse_lazy("rentals:rental-list")
