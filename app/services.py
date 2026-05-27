from django.db import transaction
from .models import Membership, Payment, MembershipPlan
from rest_framework.exceptions import ValidationError

from datetime import date, timedelta

class PaymentService:

    @staticmethod
    @transaction.atomic
    def process_payment(user, amount, plan_id):

        try:
            plan = MembershipPlan.objects.get(id=plan_id, is_active=True)
        except Membership.DoesNotExist:
            raise ValidationError({"plan": "Invalid or incative plan"})
        
        if amount != plan.price:
            raise ValidationError({"amount": "Amount does not match the plan"})

        payment = Payment.objects.create(
            user=user,
            plan=plan,
            amount=amount,
            status="SUCCESS"
        )

        start_date = date.today()

        if plan.plan_type == "MONTHLY":
            end_date = start_date + timedelta(days=30)

        elif plan.plan_type == "QUATERLY":
            end_date = start_date + timedelta(days=90)
        else:
            end_date = start_date + timedelta(days=365)

        membership = Membership.objects.create(
            user=user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
        )

        return payment, membership
