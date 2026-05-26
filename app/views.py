from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import MembershipPlan
from .serializers import MembershipPlanSerializer, RegisterSerializer
from .permissions import IsOwner, IsTrainer


class MembershipPlanViewSet(ModelViewSet):

    queryset = MembershipPlan.objects.all()

    serializer_class = MembershipPlanSerializer

    permission_classes = [IsAuthenticated, IsOwner]

class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "Registered successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )