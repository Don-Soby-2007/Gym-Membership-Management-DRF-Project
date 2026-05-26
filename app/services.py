from django.db import transaction
from .models import Membership, Payment

from datetime import date, timedelta

class PaymentService:

    @staticmethod
    @transaction.atomic
    def process_payment(user, amount, plan):

        payment = Payment.objects.create(
            user=user,
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
