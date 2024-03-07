from django.contrib.auth import get_user_model
from django.test import TestCase

from rentals.models import Insurance, Car, Rental


class ModelsTest(TestCase):
    def setUp(self):
        self.renter = get_user_model().objects.create_user(
            username="test_username",
            password="test1234"
        )
        self.insurance = Insurance.objects.create(
            name="Test Insurance",
        )
        self.car = Car.objects.create(
            model="Ford",
            year=2020,
            horsepower=200,
            daily_cost=130,
            fuel_consumption=8,
            insurance=self.insurance
        )
        self.rental = Rental.objects.create(
            car=self.car,
            renter=self.renter,
            start_date="2024-03-07",
            end_date="2024-03-17"
        )

    def test_insurance_str(self):
        self.assertEqual(str(self.insurance), self.insurance.name)

    def test_car_str(self):
        self.assertEqual(str(self.car), self.car.model)

    def test_rental_str(self):
        self.assertEqual(
            str(self.rental),
            f"Rental #{self.rental.pk} - {self.car} by {self.renter}")
