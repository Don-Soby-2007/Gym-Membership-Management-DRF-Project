from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('plans', views.MembershipPlanViewSet, basename='plans')

urlpatterns = router.urls
