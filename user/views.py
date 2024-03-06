from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from rentals.models import Rental
from user.forms import (
    RenterCreateForm,
    RenterNameAndLicenseUpdateForm,
)


class RenterListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5


class RenterDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rental_history"] = Rental.objects.filter(renter=self.object)
        return context


class RenterCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = RenterCreateForm
    success_url = reverse_lazy("user:renter-list")


class RenterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = RenterNameAndLicenseUpdateForm

    def get_success_url(self):
        return reverse_lazy("user:renter-detail", kwargs={"pk": self.object.pk})


class RenterDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("user:renter-list")
