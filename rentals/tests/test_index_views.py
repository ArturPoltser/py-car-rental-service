from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rentals.models import Insurance, Car

INDEX_URL = reverse("rentals:index")


class IndexTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234"
        )
        self.insurance = Insurance.objects.create(
            name="Test Insurance",
        )
        self.first_car = Car.objects.create(
            model="Ford",
            year=2020,
            horsepower=200,
            daily_cost=130,
            fuel_consumption=8,
            insurance=self.insurance
        )

    def test_records_counter(self):
        res = self.client.get(INDEX_URL)

        self.assertEqual(
            res.context["num_insurances"],
            Insurance.objects.all().count()
        )
        self.assertEqual(
            res.context["num_cars"],
            Car.objects.all().count()
        )
        self.assertEqual(
            res.context["num_renters"],
            get_user_model().objects.all().count()
        )
