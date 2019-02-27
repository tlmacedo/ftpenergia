import locale

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
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        context = super(LeiturasListView, self).get_context_data()
        pega_total = F('leitura')
        pega_total.output_field = FloatField()
        # qs = Energia.objects.all().annotate(sub=Sum('leitura'), total=pega_total).filter(
        #     fechamento=F('fechamento')).order_by('data').values('data', 'leitura', 'fechamento', 'total')
        qs = Energia.objects.all().annotate(total=pega_total).filter(
            fechamento=F('fechamento')).order_by('data').values('data', 'leitura', 'fechamento', 'kwh', 'total')

        dt_ultima_temp = qs[0].get('data')
        leitura_ultima_temp = qs[0].get('leitura')
        kwh = qs[0].get('kwh')
        dt_ultima_fechamento = qs[0].get('data')
        leitura_ultima_fechamento = qs[0].get('leitura')
        kwh = qs[0].get('kwh')

        linhas = []
        for linha in qs:

            linha['diff_leitura_temp'] = linha['leitura'] - leitura_ultima_temp
            linha['diff_leitura'] = linha['leitura'] - leitura_ultima_fechamento

            linha['diff_dt_temp'] = (linha['data'] - dt_ultima_temp).days
            linha['diff_dt'] = (linha['data'] - dt_ultima_fechamento).days
            try:
                diff_media_temp = linha['diff_leitura_temp'] / linha['diff_dt_temp']
            except ZeroDivisionError:
                diff_media_temp = 0

            linha['diff_media_temp'] = format(diff_media_temp, '.2f').replace('.', ',')

            try:
                diff_media = linha['diff_leitura'] / linha['diff_dt']
            except ZeroDivisionError:
                diff_media = 0

            linha['diff_media'] = format(diff_media, '.2f').replace('.', ',')

            if kwh is not None:
                linha['vlr_parcial'] = linha['diff_leitura'] * kwh
            else:
                linha['kwh'] = ' '

            dt_ultima_temp = linha['data']
            leitura_ultima_temp = linha['leitura']
            if linha['fechamento'] is True:
                dt_ultima_fechamento = linha['data']
                leitura_ultima_fechamento = linha['leitura']
                kwh = linha['kwh']

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
