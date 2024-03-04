from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Renter(AbstractUser):
    max_daily_budget = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=100,
                message="We don't have such car for this budget. Sorry."
            )
        ]
    )
    driver_license = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{2}\d{5}$",
                message="Driver license should consist only of 7 characters: "
                        "first 2 characters are uppercase letters and "
                        "last 5 characters are digits"
            )
        ]
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
