from django.shortcuts import render

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import PodsumowanieGraczy
from django.db import connection
from .forms import DateRangeForm  # poprawnie z dashboard.forms
from datetime import datetime

def podsumowanie_view(request):
    wszystkie = PodsumowanieGraczy.objects.all().order_by('gracz')
    paginator = Paginator(wszystkie, 50)  # 10 na stronę
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "barbarella_site/podsumowanie.html", {"page_obj": page_obj, "year": datetime.now().year,})

def podsumowanie_zakres(request):
    wyniki = []
    if request.method == 'GET' and 'data_od' in request.GET and 'data_do' in request.GET:
        form = DateRangeForm(request.GET)
        if form.is_valid():
            data_od = form.cleaned_data['data_od']
            data_do = form.cleaned_data['data_do']
            
            # Rzutowanie dat na typ timestamp
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM get_gracz_summary(
                        %s::timestamp, %s::timestamp
                    );
                """, [data_od, data_do])
                wyniki = cursor.fetchall()

    else:
        form = DateRangeForm()

    return render(request, 'barbarella_site/podsumowanie_zakres.html', {
        'form': form,
        'wyniki': wyniki,
    })

def podsumowanie_punkty_view(request):
    # Tymczasowo pusta logika – dodamy jak powiesz co ma się dziać
    return render(request, 'barbarella_site/podsumowanie_punkty.html')

def podsumowanie_punkty_view(request):
    form = DateRangeForm(request.GET or None)
    wyniki = []
    tabela = {}
    lochy_set = set()
    
    if form.is_valid():
        data_od = form.cleaned_data['data_od']
        data_do = form.cleaned_data['data_do']

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM get_lochy_punkty_summary(%s, %s)
            """, [data_od, data_do])
            rows = cursor.fetchall()

        # Przekształcenie wyników do dicta
        for gracz, nazwa_lochu, ilosc, punkty in rows:
            lochy_set.add(nazwa_lochu)
            if gracz not in tabela:
                tabela[gracz] = {'lochy': {}, 'suma': 0, 'punkty': 0}
            tabela[gracz]['lochy'][nazwa_lochu] = ilosc
            tabela[gracz]['suma'] += ilosc
            tabela[gracz]['punkty'] += punkty

        lochy_list = sorted(lochy_set)
        wyniki = tabela.items()

    return render(request, 'barbarella_site/podsumowanie_punkty.html', {
        'form': form,
        'lochy_list': lochy_list if form.is_valid() else [],
        'wyniki': wyniki
    })