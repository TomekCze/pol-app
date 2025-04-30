from django import forms
from django.db import connection


class DateRangeForm(forms.Form):
    data_od = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data od"
    )
    data_do = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data do"
    )
    klan = forms.ChoiceField(
        choices=[],
        label="Klan",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Wczytaj listę klanów z bazy danych
        with connection.cursor() as cursor:
            cursor.execute("SELECT nazwa_skrot FROM klany ORDER BY nazwa_skrot")
            klany = cursor.fetchall()
        self.fields['klan'].choices = [('', 'Wybierz klan')] + [(k[0], k[0]) for k in klany]