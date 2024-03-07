from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

RENTER_LIST_URL = reverse("user:renter-list")
RENTER_CREATE_URL = reverse("user:renter-create")
RENTER_DETAIL_URL = reverse("user:renter-detail", kwargs={"pk": 1})
RENTER_UPDATE_URL = reverse("user:renter-update", kwargs={"pk": 1})
RENTER_DELETE_URL = reverse("user:renter-delete", kwargs={"pk": 1})


class PublicRenterTest(TestCase):

    def test_login_required(self):
        for url in (
                RENTER_LIST_URL,
                RENTER_CREATE_URL,
                RENTER_DETAIL_URL,
                RENTER_UPDATE_URL,
                RENTER_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class RenterPrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
            driver_license="TE12345"
        )
        self.client.force_login(self.user)

        self.renter = get_user_model().objects.create_user(
            username="renter_username",
            password="test1234",
            driver_license="TS12345"
        )

    def test_retrieve_renters(self):
        res = self.client.get(RENTER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["renter_list"]),
            list(get_user_model().objects.all())
        )
        self.assertTemplateUsed(res, "user/renter_list.html")

    def test_renter_search_filter(self):
        url = f"{RENTER_LIST_URL}?username=rent"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(list(res.context["renter_list"]), [self.renter])
