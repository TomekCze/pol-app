"""
URL configuration for django_bulma_supabase_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from barbarella_site.views import podsumowanie_view, podsumowanie_zakres, podsumowanie_punkty_view, index_view, weekly_norms_view, scoring_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index_view, name="index"),
    path('podsumowanie/', podsumowanie_zakres, name='podsumowanie_zakres'),
    path('punkty/', podsumowanie_punkty_view, name='podsumowanie_punkty'),
    path('scoring/', scoring_view, name='scoring'),
    path('weekly-norms/', weekly_norms_view, name='weekly_norms'),
]
