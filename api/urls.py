from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .produtor_rural.views import ProdutorRuralViewSet, CulturaViewSet

router = DefaultRouter()
router.register(r'produtor_rural', ProdutorRuralViewSet)
router.register(r'cultura', CulturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
