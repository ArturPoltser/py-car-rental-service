from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rentals.models import Insurance

INSURANCE_LIST_URL = reverse("rentals:insurance-list")
INSURANCE_CREATE_URL = reverse("rentals:insurance-create")
INSURANCE_UPDATE_URL = reverse("rentals:insurance-update", kwargs={"pk": 1})
INSURANCE_DELETE_URL = reverse("rentals:insurance-delete", kwargs={"pk": 1})


class InsurancePublicTest(TestCase):

    def test_login_required(self):
        for url in (
                INSURANCE_LIST_URL,
                INSURANCE_CREATE_URL,
                INSURANCE_UPDATE_URL,
                INSURANCE_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class InsurancePrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
        )
        self.client.force_login(self.user)
        self.first_insurance = Insurance.objects.create(
            name="Test First Insurance",
        )
        self.second_insurance = Insurance.objects.create(
            name="Test Second Insurance",
        )

    def test_retrieve_insurances(self):
        res = self.client.get(INSURANCE_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["insurance_list"]),
            list(Insurance.objects.all())
        )
        self.assertTemplateUsed(res, "rentals/insurance_list.html")

    def test_insurances_search_filter(self):
        url = f"{INSURANCE_LIST_URL}?name=se"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(
            list(res.context["insurance_list"]),
            [self.second_insurance]
        )
