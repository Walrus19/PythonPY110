from django.contrib import admin
from django.urls import path, include
from random import random
from django.http import HttpResponse
from app_datetime.views import datetime_view
from datetime import datetime
# from weather_api import current_weather
from store.views import products_view, shop_view

def datetime_view(request):
    if request.method == "GET":
        data = datetime.now()
        return HttpResponse(data)
def random_view(request):
    if request.method == "GET":
        data = random()
        return HttpResponse(data)

from django.http import JsonResponse

# def weather(request):
#     if request.method == "GET":
#         data = current_weather(40, 30)
#         # Результат работы функции current_weather
#         # А возвращаем объект JSON. Параметр json_dumps_params используется, чтобы передать ensure_ascii=False
#         # как помните это необходимо для корректного отображения кириллицы
#         return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
#                                                      'indent': 4})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('random/', random_view),
    path('datetime/', datetime_view),
    path('weather/', include('app_weather.urls')),
    # path('weather/', weather),
    # path('product/', products_view),
    # path('', shop_view)
    path('', include('store.urls')),
    path('login/', include('app_login.urls'))
    ]