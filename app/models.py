from django.db import models

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