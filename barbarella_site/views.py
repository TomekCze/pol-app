from django.shortcuts import render

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import PodsumowanieGraczy, Scoring
from django.db import connection
from .forms import DateRangeForm  # poprawnie z dashboard.forms
from datetime import datetime, timedelta

# Strona główna - tylko obrazek
def index_view(request):
    return render(request, 'barbarella_site/index.html')

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

#Sekcja CHESTS - SPECIFICALLY
def podsumowanie_punkty_view(request):
    form = DateRangeForm(request.GET or None)
    wyniki = []
    tabela = {}
    lochy_dict = {}  # Będzie zawierać: {nazwa_lochu: sort}
    
    if form.is_valid():
        data_od = form.cleaned_data['data_od']
        data_do = form.cleaned_data['data_do']
        klan = form.cleaned_data.get('klan')  # Może być None

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM get_lochy_punkty_summary(%s::timestamp, %s::timestamp, %s::TEXT)
            """, [data_od, data_do, klan])
            rows = cursor.fetchall()

        for gracz, nazwa_lochu, ilosc, punkty, sort in rows:
            lochy_dict[nazwa_lochu] = sort
            if gracz not in tabela:
                tabela[gracz] = {'lochy': {}, 'suma': 0, 'punkty': 0}
            tabela[gracz]['lochy'][nazwa_lochu] = ilosc
            tabela[gracz]['suma'] += ilosc
            tabela[gracz]['punkty'] += punkty

        # Sortujemy lochy według pola sort z funkcji
        lochy_list = [nazwa for nazwa, _ in sorted(lochy_dict.items(), key=lambda x: x[1])]
        wyniki = tabela.items()

    return render(request, 'barbarella_site/podsumowanie_punkty.html', {
        'form': form,
        'lochy_list': lochy_list if form.is_valid() else [],
        'wyniki': wyniki
    })
#KONIEC Sekcja CHESTS - SPECIFICALLY

#sekcja dla weekly norms
def weekly_norms_view(request):
    # Pobieranie wybranego klanu z zapytania GET
    selected_klan = request.GET.get("klan")

    # Pobierz listę klanów (zwracamy tylko skroty klanów)
    with connection.cursor() as cursor:
        cursor.execute("SELECT nazwa_skrot FROM klany ORDER BY nazwa_skrot")
        klany = [row[0] for row in cursor.fetchall()]

    gracze = []
    zakresy = []

    if selected_klan:
        # Używamy funkcji `get_weekly_summary_by_klan` zamiast bezpośredniego zapytania do widoku
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM get_weekly_summary_by_klan(%s)
            """, [selected_klan])
            rows = cursor.fetchall()

        # Przetwarzamy dane o graczach
        for row in rows:
            gracz = row[0]
            tygodnie = []
            for i in range(7):  # 7 tygodni (indeks 1 + 6 tygodni danych)
                index = 1 + i * 3
                tygodnie.append({
                    "skrzynki": row[index],
                    "punkty": row[index + 1],
                    "zakres": row[index + 2],
                })
            gracze.append({
                "gracz": gracz,
                "tygodnie": tygodnie
            })

        # Wyciągamy zakresy tygodni dla graczy
        for g in gracze:
            if all("zakres" in t and t["zakres"] for t in g["tygodnie"]):
                zakresy = [t["zakres"] for t in g["tygodnie"]]
                break  # Zakresy są wspólne dla wszystkich graczy

    # Renderujemy stronę z danymi
    return render(request, "barbarella_site/weekly_norms.html", {
        "gracze": gracze,
        "zakresy": zakresy,
        "klany": klany,
        "selected_klan": selected_klan
    })
"""
def weekly_norms_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM weekly_summary_last_6")  # Upewnij się, że to Twoja nazwa widoku w Supabase
        rows = cursor.fetchall()

    # Zakładamy, że kolumny są w tej kolejności:
    # gracz, liczba_skrzyn_1, liczba_punktow_1, zakres_1, liczba_skrzyn_2, liczba_punktow_2, zakres_2, ..., zakres_6
    gracze = []
    for row in rows:
        gracz = row[0]
        tygodnie = []
        for i in range(6):  # 6 tygodni
            index = 1 + i * 3
            tygodnie.append({
                "skrzynki": row[index],
                "punkty": row[index + 1],
                "zakres": row[index + 2],
            })
        gracze.append({
            "gracz": gracz,
            "tygodnie": tygodnie
        })

    # ✅ Nowe: wyciągamy zakresy tygodni z pierwszego gracza, który ma je w pełni
    zakresy = []
    for g in gracze:
        if all("zakres" in t and t["zakres"] for t in g["tygodnie"]):
            zakresy = [t["zakres"] for t in g["tygodnie"]]
            break

    return render(request, "barbarella_site/weekly_norms.html", {
        "gracze": gracze,
        "zakresy": zakresy
    })
"""
#koniec sekcja weekly norms

#Początek scoring
def scoring_view(request):
    dane = Scoring.objects.all()
    return render(request, 'barbarella_site/scoring.html', {'dane': dane})
#Koniec scoring

#Poczatek tinman
def tinman_view(request):
    # Tymczasowo pusta logika – dodamy jak powiesz co ma się dziać
    return render(request, 'barbarella_site/tinman.html')
#Koniec tinman