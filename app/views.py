from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MembershipPlan
from .serializers import MembershipPlanSerializer, RegisterSerializer


class MembershipPlanViewSet(ModelViewSet):

    queryset = MembershipPlan.objects.all()

    serializer_class = MembershipPlanSerializer

class RegisterAPIView(APIView):

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