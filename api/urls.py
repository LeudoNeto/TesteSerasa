from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .produtor_rural.views import ProdutorRuralViewSet, CulturaViewSet
from .dashboard.views import DashboardAPIView

router = DefaultRouter()
router.register(r'produtor_rural', ProdutorRuralViewSet)
router.register(r'cultura', CulturaViewSet)
router.register(r'dashboard', DashboardAPIView, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
