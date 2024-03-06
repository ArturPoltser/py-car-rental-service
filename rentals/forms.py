from django import forms
from rentals.models import Rental, Car


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ("start_date", "end_date")

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        overlapping_rentals = Rental.objects.filter(
            car=cleaned_data.get("car"),
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if overlapping_rentals.exists():
            occupied_dates = overlapping_rentals.values_list(
                "start_date",
                "end_date"
            )
            occupied_dates_list = [
                f"from {start_date} to {end_date}"
                for start_date, end_date in occupied_dates
            ]
            raise forms.ValidationError(
                "The selected dates are already occupied. "
                f"Occupied dates: {', '.join(occupied_dates_list)}."
            )


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by model"})
    )


class InsuranceSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by model"})
    )
