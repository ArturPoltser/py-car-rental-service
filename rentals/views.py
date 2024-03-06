from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from rentals.forms import RentalForm, CarSearchForm, InsuranceSearchForm
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
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = InsuranceSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Insurance.objects.all()
        form = InsuranceSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


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
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["search_form"] = CarSearchForm(
            initial={"model": model}
        )
        return context

    def get_queryset(self):
        queryset = Car.objects.select_related("insurance")
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(model__icontains=form.cleaned_data["model"])
        return queryset


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
    model = Rental
    context_object_name = "rentals"

    def get_queryset(self):
        queryset = Rental.objects.select_related("renter")
        car = get_object_or_404(Car, pk=self.kwargs["pk"])
        return queryset.filter(car=car)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car"] = get_object_or_404(Car, pk=self.kwargs["pk"])
        return context


@login_required
def rental_create_view(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.car = car
            rental.renter = request.user
            rental.save()
            return redirect("rentals:car-detail", pk=pk)

    form = RentalForm()
    context = {"car": car, "form": form}
    return render(request, "rentals/rental_create.html", context)


@login_required
def rental_detail_view(request, pk, r_pk):
    car_id = pk
    rental = get_object_or_404(Rental, car_id=car_id, pk=r_pk)
    context = {"rental": rental}
    return render(request, "rentals/rental_detail.html", context)


@login_required
def rental_update_view(request, pk, r_pk):
    car_id = pk
    rental = get_object_or_404(Rental, car_id=car_id, pk=r_pk)
    form = RentalForm(request.POST, instance=rental)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("rentals:rental-list", pk=car_id)

    context = {"form": form, "rental": rental}
    return render(request, "rentals/rental_update.html", context)


@login_required
def rental_delete_view(request, pk, r_pk):
    car_id = pk
    rental = get_object_or_404(Rental, car_id=car_id, pk=r_pk)

    if request.method == "POST":
        rental.delete()
        return redirect("rentals:rental-list", pk=car_id)

    context = {"rental": rental}
    return render(request, "rentals/rental_confirm_delete.html", context)
