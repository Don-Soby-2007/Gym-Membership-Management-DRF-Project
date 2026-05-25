from rest_framework import serializers
from . import models

class MembershipPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MembershipPlan
        fields = '__all__'