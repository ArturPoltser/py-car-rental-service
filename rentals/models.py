from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Insurance(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Car(models.Model):
    model = models.CharField(max_length=255)
    year = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=2005,
                message="Year should be from 2005 onwards."
            ),
            MaxValueValidator(
                limit_value=2023,
                message="Year should not exceed 2023."
            )
        ]
    )
    horsepower = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=100,
                message="We can't rent car with less than 100 horsepowers."
            ),
            MaxValueValidator(
                limit_value=800,
                message="We can't rent car with more than 800 horsepowers."
            )
        ]
    )
    fuel_consumption = models.IntegerField()
    daily_cost = models.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=100,
                message="We can't rent car with daily price less than 100$."
            ),
            MaxValueValidator(
                limit_value=2000,
                message="We can't rent car with daily price more than 2000$."
            )
        ]
    )
    available_to_rent = models.BooleanField(default=True)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)

    def __str__(self):
        return self.model


class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Rental #{self.pk} - {self.car} by {self.renter}"
