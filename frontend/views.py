from django.views.generic import TemplateView
from api.produtor_rural.models import ProdutorRural

class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Página Inicial'
        context['link_atual'] = 'index'

        return context
    
class ProdutoresRuraisView(TemplateView):
    template_name = 'produtores_rurais/produtores_rurais.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = 'Produtores Rurais'
        context['link_atual'] = 'produtores_rurais'

        context['produtores_rurais'] = ProdutorRural.objects.all()

        return context