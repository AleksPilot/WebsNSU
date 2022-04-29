# django_web_scraping_example/views.pyfrom django.shortcuts import render
from django.views import generic
# Создаем представление здесь.
class HomePageView(generic.ListView):
    template_name = 'home.html'
