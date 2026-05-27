from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

router.register('plans', views.MembershipPlanViewSet, basename='plans')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh', TokenRefreshView.as_view(), name='login_refresh'),

    path('register/', views.RegisterAPIView.as_view(), name='register'),

    path('users/', views.UserListView.as_view(), name='users'),

    path('payment/', views.PaymentAPIView.as_view(), name='payment'),
    path('payment/history/', views.PaymentHistoryAPIView.as_view(), name='payment-history'),
    path('payment/history/<int:user_id>/', views.PaymentHistoryAPIView.as_view(), name='payment-history-user'),

    path('', include(router.urls)),
]
