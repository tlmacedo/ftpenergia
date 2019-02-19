from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from energia.Forms import LeiturasForm
from energia.models import Energia


class LeiturasListView(ListView):
    template_name = 'energia/leituras.html'
    model = Energia
    context_object_name = 'leituras'




class LeituraCreateView(CreateView):
    template_name = 'energia/leitura_adicionar.html'
    model = Energia
    form_class = LeiturasForm
    success_url = reverse_lazy('energia:leitura_lista')
