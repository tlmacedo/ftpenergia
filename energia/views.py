from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import F, Min, FloatField, Sum

from energia.Forms import LeiturasForm
from energia.models import Energia


class LeiturasListView(ListView):
    template_name = 'energia/leituras.html'
    model = Energia
    context_object_name = 'leituras'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeiturasListView, self).get_context_data()
        pega_total = F('leitura')
        pega_total.output_field = FloatField()
        # qs = Energia.objects.all().annotate(sub=Sum('leitura'), total=pega_total).filter(
        #     fechamento=F('fechamento')).order_by('data').values('data', 'leitura', 'fechamento', 'total')
        qs = Energia.objects.all().annotate(sub=Sum('leitura'), total=pega_total).filter(
            fechamento=F('fechamento')).order_by('data').values('data', 'leitura', 'fechamento', 'total')

        dt_ultima_temp = qs[0].get('data')
        leitura_ultima_temp = 20321

        linhas = []
        for linha in qs:
            # if linha['fechamento'] is True:
            #     dt_ultima_fechamento = linha['data']
            #     leitura_ultima_fechamento = linha['leitura']

            # leitura = linha['leitura']
            # if leitura > leitura_ultima_temp:
            # diff_leitura_temp = linha['leitura'] - leitura_ultima_temp
            # else:
            #     diff_leitura_temp = 0
            # diff_data = linha['data'] - dt_ultima_temp
            linha['diff_leitura_temp'] = linha['leitura'] - leitura_ultima_temp
            linha['diff_dt_temp'] = (linha['data'] - dt_ultima_temp).days
            try:
                diff_media_temp = linha['diff_leitura_temp'] / linha['diff_dt_temp']
            except ZeroDivisionError:
                diff_media_temp = 0

            linha['diff_media_temp'] = diff_media_temp

            dt_ultima_temp = linha['data']
            leitura_ultima_temp = linha['leitura']

            # parcial_temp = leitura_ultima_fechamento - linha['leitura']
            # linha['dias'] = 0
            linhas.append(linha)
        # if ultimo_fech is not False and parcial != 0:
        #     linhas.append({'subtotal': parcial})
        #     parcial = 0
        # linha['parcial'] = 1
        # linha['dias'] = 2
        # linhas.append(linha)
        # ultimo_fech = linha['fechamento']
        # subtotal += linha['total']
        # total += linha['total']

        # if ultimo_fech is not False:
        #     linhas.append({'subtotal': subtotal})
        # linhas.append({'total': total})

        context['linhas'] = linhas
        return context


class LeituraCreateView(CreateView):
    template_name = 'energia/leitura_adicionar.html'
    # model = Energia
    form_class = LeiturasForm
    success_url = reverse_lazy('energia:leitura_lista')
