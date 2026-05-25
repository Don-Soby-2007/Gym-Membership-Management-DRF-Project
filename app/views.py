from rest_framework.viewsets import ModelViewSet
from .models import MembershipPlan
from .serializers import MembershipPlanSerializer


class MembershipPlanViewSet(ModelViewSet):

    queryset = MembershipPlan.objects.all()

    serializer_class = MembershipPlanSerializer
