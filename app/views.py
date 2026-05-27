from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import MembershipPlan, User
from .serializers import MembershipPlanSerializer, UserSerializer, PaymentSerilizer
from .permissions import IsAdmin
from .services import PaymentService
from django.shortcuts import get_object_or_404


class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "Registered successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})
    
class PaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = PaymentSerilizer(data=request.data)

        serializer.is_valid(raise_exception=True)

        plan_id = serializer.validated_data['plan'].id
        amount = serializer.validated_data["amount"]

        payment, membership = PaymentService.process_payment(
            user=request.user,
            amount=amount,
            plan_id=plan_id
        )

        return Response(
            {
                "message": "Payment successful",
                "payment_id": payment.id,
                "amount": payment.amount,
                "membership_end_date": membership.end_date,
            }, status=status.HTTP_201_CREATED
        )