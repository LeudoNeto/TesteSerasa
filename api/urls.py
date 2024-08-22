from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .produtor_rural.views import ProdutorRuralViewSet, CulturaViewSet
from .dashboard.views import DashboardAPIView

# Configuração do schema Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Brain Agriculture",
        default_version='v1',
        description="Documentação da API para gestão de produtores rurais e culturas.",
    ),
    public=True,
)

router = DefaultRouter()
router.register(r'produtor_rural', ProdutorRuralViewSet)
router.register(r'cultura', CulturaViewSet)
router.register(r'dashboard', DashboardAPIView, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
