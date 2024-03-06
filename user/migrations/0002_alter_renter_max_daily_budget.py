# Generated by Django 5.0.3 on 2024-03-05 10:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='max_daily_budget',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(limit_value=100, message="We don't have such car for this budget. Sorry.")]),
        ),
    ]