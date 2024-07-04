from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, TaskViewSet, AttributesViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'attributes', AttributesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]