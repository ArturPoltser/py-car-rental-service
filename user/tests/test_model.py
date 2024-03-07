from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):
    def test_renter_str(self):
        renter = get_user_model().objects.create_user(
            username="test_username",
            password="test1234"
        )
        self.assertEqual(
            str(renter),
            f"{renter.username} ({renter.first_name} {renter.last_name})"
        )