from django.db import models


class Energia(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.DateTimeField(db_column='data', blank=True, null=True)
    leitura = models.IntegerField(unique=True)
    fechamento = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'energia'
