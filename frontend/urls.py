from django.urls import path

from .views import IndexView, ProdutoresRuraisView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('produtores_rurais/', ProdutoresRuraisView.as_view(), name='produtores_rurais'),
]