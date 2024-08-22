from rest_framework import viewsets
from .models import ProdutorRural
from .serializers import ProdutorRuralSerializer

class ProdutorRuralViewSet(viewsets.ModelViewSet):
    queryset = ProdutorRural.objects.all()
    serializer_class = ProdutorRuralSerializer
