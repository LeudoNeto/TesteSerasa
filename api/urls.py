from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .produtor_rural.views import ProdutorRuralViewSet

router = DefaultRouter()
router.register(r'produtor_rural', ProdutorRuralViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
