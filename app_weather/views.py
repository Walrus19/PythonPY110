from django.shortcuts import render
from django.http import JsonResponse
# from .models import DATABASE
from django.http import HttpResponse
from weather_api import current_weather

def weather(request):
    if request.method == "GET":
        data = current_weather(40, 30)
        # Результат работы функции current_weather
        # А возвращаем объект JSON. Параметр json_dumps_params используется, чтобы передать ensure_ascii=False
        # как помните это необходимо для корректного отображения кириллицы
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
