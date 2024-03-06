from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RenterCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "driver_license",
            "first_name",
            "last_name",
        )


class RenterNameAndLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["driver_license", "first_name", "last_name"]
