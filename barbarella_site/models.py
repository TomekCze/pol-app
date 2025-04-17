from django.db import models

class PodsumowanieGraczy(models.Model):
    gracz = models.TextField(primary_key=True)
    ilosc = models.IntegerField()

    class Meta:
        managed = False  # bo to widok w bazie danych
        db_table = 'podsumowanie_graczy'