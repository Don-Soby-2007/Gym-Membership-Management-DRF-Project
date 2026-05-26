from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MembershipPlan(models.Model):

    PLAN_TYPES = (
        ('MONTHLY', 'Monthly'),
        ('QUATERLY', 'Quaterly'),
        ('YEARLY', 'Yearly'),
    )

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)

    is_active = models.BooleanField(default=True)


class User(AbstractUser):

    ROLE_CHOICES = (
        ('USER', 'User'),
        ('GYM_TRAINER', 'Gym Trainer'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

class Membership(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')

    plan = models.OneToOneField(MembershipPlan, on_delete=models.CASCADE, related_name='plan')

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
    

class Payment(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"