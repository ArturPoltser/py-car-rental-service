from django import forms
from rentals.models import Rental


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ("start_date", "end_date", "car")

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "car": forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date < start_date:
            raise forms.ValidationError("End date must not be earlier than the start date.")

        total_period = (end_date - start_date).days
        if total_period > 30:
            raise forms.ValidationError("The total rental period must not exceed 30 days.")

        car = cleaned_data.get("car")
        overlapping_rentals = Rental.objects.filter(
            car=car,
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if overlapping_rentals.exists():
            occupied_dates = overlapping_rentals.values_list(
                "start_date",
                "end_date"
            )
            occupied_dates_list = [
                f"from {start} to {end}"
                for start, end in occupied_dates
            ]
            raise forms.ValidationError(
                f"The selected dates are already occupied. Occupied dates: {', '.join(occupied_dates_list)}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


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
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
