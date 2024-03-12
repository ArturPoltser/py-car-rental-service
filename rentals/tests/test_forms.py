from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from rentals.forms import RentalForm, CarSearchForm, InsuranceSearchForm
from rentals.models import Rental, Car, Insurance


class RentalFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
        )
        self.client.force_login(self.user)
        self.insurance = Insurance.objects.create(name="Test Insurance")
        self.car = Car.objects.create(
            model="Ford",
            year=2020,
            horsepower=200,
            daily_cost=130,
            fuel_consumption=8,
            insurance=self.insurance
        )

    def test_rental_form_clean_method(self):
        Rental.objects.create(
            car=self.car,
            renter=self.user,
            start_date="2024-03-07",
            end_date="2024-03-17",
        )

        form_data = {
            "car": self.car,
            "renter": self.user,
            "start_date": "2024-03-10",
            "end_date": "2024-03-17",
        }
        form = RentalForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            "".join(form.errors["__all__"]),
            "The selected dates are already occupied. "
            "Occupied dates: from 2024-03-07 to 2024-03-17."
        )

    def test_rental_form_clean_method_valid(self):
        form_data = {
            "car": self.car,
            "start_date": date(2024, 3, 20),
            "end_date": date(2024, 3, 25),
        }
        form = RentalForm(data=form_data)

        self.assertTrue(form.is_valid())


class CarSearchFormTest(TestCase):
    def test_car_search_form(self):
        form_data = {
            "model": "Test Model"
        }
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())


class InsuranceSearchFormTest(TestCase):
    def test_insurance_search_form(self):
        form_data = {
            "name": "Test Insurance"
        }
        form = InsuranceSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
