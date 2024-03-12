from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rentals.models import Car, Rental, Insurance

RENTAL_LIST_URL = reverse("rentals:rental-list", kwargs={"pk": 1})
RENTAL_CREATE_URL = reverse("rentals:rental-create", kwargs={"pk": 1})
RENTAL_DETAIL_URL = reverse(
    "rentals:rental-detail",
    kwargs={"pk": 1, "r_pk": 1}
)
RENTAL_UPDATE_URL = reverse(
    "rentals:rental-update",
    kwargs={"pk": 1, "r_pk": 1}
)
RENTAL_DELETE_URL = reverse(
    "rentals:rental-delete",
    kwargs={"pk": 1, "r_pk": 1}
)


class RentalListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
        )
        self.client.force_login(self.user)
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
            renter=self.user,
            start_date="2024-03-07",
            end_date="2024-03-17"
        )

    def test_retrieve_rental(self):
        res = self.client.get(RENTAL_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["rentals"]),
            list(Rental.objects.all())
        )
        self.assertTemplateUsed(res, "rentals/rental_list.html")

    def test_rental_create_view_uses_correct_template(self):
        res = self.client.get(RENTAL_CREATE_URL)
        self.assertTemplateUsed(res, "rentals/rental_create.html")

    def test_rental_detail_view_uses_correct_template(self):
        res = self.client.get(RENTAL_DETAIL_URL)
        self.assertTemplateUsed(res, "rentals/rental_detail.html")

    def test_rental_update_view_uses_correct_template(self):
        res = self.client.get(RENTAL_UPDATE_URL)
        self.assertTemplateUsed(res, "rentals/rental_update.html")

    def test_rental_delete_view_uses_correct_template(self):
        res = self.client.get(RENTAL_DELETE_URL)
        self.assertTemplateUsed(res, "rentals/rental_confirm_delete.html")
