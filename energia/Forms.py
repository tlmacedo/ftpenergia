from django import forms

from energia.models import *


class LeiturasForm(forms.ModelForm):
    # data = forms.DateTimeField(
    #     label='data',
    #     required='True',
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'text-right date_time',
    #         }),
    # )
    #
    # leitura = forms.IntegerField(
    #     label='leitura',
    #     required='True',
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'text-right numero6mil',
    #         }),
    # )
    #
    # fechamento = forms.CheckboxInput(
    #     label='fechamento',
    #     widget=forms.CheckboxInput(
    #     )
    # )
    #
    class Meta:
        model = Energia
        exclude = ('id',)
        help_texts = {
            'data': 'Informe a data de leitura.',
            'leitura': 'Informe o valor da leitura.',
            'fechamento': 'Essa leitura foi fechamento de mês?',
        }
        widgets = {
            'data': forms.TextInput(attrs={'class': 'text-right msk-data_hora'}),
            'leitura': forms.TextInput(attrs={'class': 'text-right msk-numero6mil'}),
            'fechamento': forms.CheckboxInput(attrs={}),
        }

    # model = Energia
    #
    # fields = '__all__'
