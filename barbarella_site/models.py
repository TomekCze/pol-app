from django.db import models

class PodsumowanieGraczy(models.Model):
    gracz = models.TextField(primary_key=True)
    ilosc = models.IntegerField()

    class Meta:
        managed = False  # bo to widok w bazie danych
        db_table = 'podsumowanie_graczy'

class Scoring(models.Model):
    chests = models.CharField(max_length=200, primary_key=True)
    points = models.IntegerField()

    class Meta:
        managed = False  # Ważne! Bo to widok SQL, nie tabela.
        db_table = 'scoring'