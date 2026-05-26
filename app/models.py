from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MembershipPlan(models.Model):

    PLAN_TYPES = (
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
        ('VIP', 'VIP'),
    )

    name = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)

    is_active = models.BooleanField(default=True)


class User(AbstractUser):

    ROLE_CHOICES = (
        ('USER', 'User'),
        ('GYM_OWNER', 'Gym Owner'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )