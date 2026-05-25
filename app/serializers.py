from rest_framework import serializers
from . import models

class MembershipPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MembershipPlan
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('The price should be greater than Zero')
        return value
    
    def validate(self, attrs):

        duration = attrs['duration']
        plan_type = attrs['plan_type']

        if plan_type == 'VIP':
            if duration != 30:
                raise serializers.ValidationError('VIP plan only have duration of 30 days')
        return super().validate(attrs)
