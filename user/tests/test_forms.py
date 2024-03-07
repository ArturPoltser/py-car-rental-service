from django.test import TestCase

from user.forms import (
    RenterCreateForm,
    RenterNameAndLicenseUpdateForm,
    RenterSearchForm,
)


class CreateDriverFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_username",
            "password1": "test_password123",
            "password2": "test_password123",
            "first_name": "first_test",
            "last_name": "last_test",
        }

    def test_driver_creation_form_with_valid_license(self):
        self.form_data["driver_license"] = "TE12345"
        form = RenterCreateForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_invalid_license(self):
        for driver_license in ["ab12345", "ABCDEFGH", "AB1234"]:
            self.form_data["driver_license"] = driver_license
            form = RenterCreateForm(data=self.form_data)

            self.assertFalse(form.is_valid())

    def test_driver_creation_form_without_license(self):
        form = RenterCreateForm(self.form_data)

        self.assertFalse(form.is_valid())


class UpdateDriverFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "test_username",
            "password1": "test_password123",
            "password2": "test_password123",
            "first_name": "first_test",
            "last_name": "last_test",
            "driver_license": "AB12345"
        }
        self.form = RenterCreateForm(data=self.form_data)

    def test_update_form_with_valid_license(self):
        self.form = RenterNameAndLicenseUpdateForm(
            data={"driver_license": "TE54321"}
        )

        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data["driver_license"], "TE54321")

    def test_update_form_with_invalid_license(self):
        for driver_license in ["ab12345", "ABCDEFGH", "AB1234"]:
            self.form = RenterCreateForm(
                data={"driver_license": driver_license}
            )

            self.assertFalse(self.form.is_valid())
            self.assertNotIn("driver_license", self.form.cleaned_data)
            self.assertEqual(self.form.data["driver_license"], driver_license)

    def test_update_form_without_data(self):
        self.form = RenterNameAndLicenseUpdateForm(
            data={"driver_license": ""}
        )

        self.assertFalse(self.form.is_valid())
        self.assertNotIn("driver_license", self.form.cleaned_data)
        self.assertEqual(self.form.data["driver_license"], "")


class RenterSearchFormTest(TestCase):
    def setUp(self):
        self.form = RenterSearchForm()

    def test_model_field_placeholder(self):
        self.assertEqual(
            self.form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )

    def test_model_field_not_required(self):
        self.assertFalse(self.form.fields["username"].required)
