from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import MembershipPlan, User, Payment
from .serializers import MembershipPlanSerializer, UserSerializer, PaymentSerilizer
from .permissions import IsAdmin, IsSelfOrAdmin, IsTrainerOrAdmin
from .services import PaymentService
from .pagination import PaginationClass
from rest_framework_simplejwt.tokens import RefreshToken


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
    
class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsTrainerOrAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.filter(role='USER')

class PaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        plans = MembershipPlan.objects.filter(is_active=True)

        paginator = PaginationClass()

        page = paginator.paginate_queryset(plans, request)

        serializer = MembershipPlanSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
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

class PaymentHistoryAPIView(APIView):

    permission_classes = [IsAuthenticated, IsSelfOrAdmin]

    def get(self, request, user_id=None):

        if request.user.role == 'ADMIN':
            if user_id:
                payments = Payment.objects.filter(user_id=user_id)
            else:
                payments = Payment.objects.all()

        else:
            if user_id and int(user_id) != request.user.id:
                return Response({
                    "detail": "You do not have permission to view this user's history"
                }, status=status.HTTP_403_FORBIDDEN)
            
            payments = Payment.objects.filter(user=request.user)

        serializer = PaymentSerilizer(payments, many=True)
        return Response({"payments": serializer.data})
    
class MembershipPlanViewSet(ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    
    def get_permissions(self):
        
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        
        return [permission() for permission in permission_classes]

class LogoutAPIView(APIView):

    def post(self, request):

        refresh = request.data.get('refresh')

        token = RefreshToken(refresh)

        token.blacklist()

        return Response(
            {'message': "Logged out successfully"},
            status=status.HTTP_200_OK
        )