from django.db import connection

def latest_lochy_date(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(data_utworzenia) + INTERVAL '2 hours' FROM lochy")
        row = cursor.fetchone()
    return {
        "latest_lochy_date": row[0] if row else None
    }