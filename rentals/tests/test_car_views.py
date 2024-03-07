from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rentals.models import Car, Insurance

CAR_LIST_URL = reverse("rentals:car-list")
CAR_CREATE_URL = reverse("rentals:car-create")
CAR_DETAIL_URL = reverse("rentals:car-detail", kwargs={"pk": 1})
CAR_UPDATE_URL = reverse("rentals:car-update", kwargs={"pk": 1})
CAR_DELETE_URL = reverse("rentals:car-delete", kwargs={"pk": 1})


class CarPublicTest(TestCase):

    def test_login_required(self):
        for url in (
                CAR_LIST_URL,
                CAR_CREATE_URL,
                CAR_DETAIL_URL,
                CAR_UPDATE_URL,
                CAR_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class CarPrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234"
        )
        self.client.force_login(self.user)
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
        self.second_car = Car.objects.create(
            model="Audi",
            year=2020,
            horsepower=500,
            daily_cost=250,
            fuel_consumption=15,
            insurance=self.insurance
        )

    def test_retrieve_cars(self):
        res = self.client.get(CAR_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["car_list"]),
            list(Car.objects.all())
        )
        self.assertTemplateUsed(res, "rentals/car_list.html")

    def test_cars_search_filter(self):
        url = f"{CAR_LIST_URL}?model=fo"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(list(res.context["car_list"]), [self.first_car])
