from rest_framework import serializers
from .models import User, MembershipPlan, Payment

class MembershipPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = MembershipPlan
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('The price should be greater than Zero')
        return value


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

        read_only_fields = ['id', 'role']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data['email'],
            password=validated_data['password'],
            role="USER",
        )

        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        return data


class PaymentSerilizer(serializers.ModelSerializer):

    class Meta:

        model = Payment
        fields = ["id", "user", "plan", "amount", "status", "payment_date"]
        read_only_fields = ["user", "status", "payment_date"]

        def validate_amount(self, value):
            if value <= 0:
                raise serializers.ValidationError("Amount must be positive.")
            return value
        