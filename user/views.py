from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic


class RenterListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 5


class RenterDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


class RenterCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    fields = "__all__"
    success_url = reverse_lazy("")


class RenterUpdateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    fields = "__all__"
    success_url = reverse_lazy("")


class RenterDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("")
