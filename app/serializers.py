from rest_framework import serializers
from .models import User, MembershipPlan

class MembershipPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = MembershipPlan
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


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User
        fields = ['username', 'email', 'password', 'role']

        read_only_fields = ['role']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data['email'],
            password=validated_data['password'],
            role="USER",
        )

        return user