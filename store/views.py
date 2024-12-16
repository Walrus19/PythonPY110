from django.db.models.expressions import result

from logic.services import filtering_category
from django.shortcuts import render
from django.http import JsonResponse
from store.models import DATABASE
from django.http import HttpResponse
from logic.services import view_in_cart, add_to_cart, remove_from_cart

# def products_view(request):
#     if request.method == "GET":
#         return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
#                                                      'indent': 4})
        # Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
        # как в приложении app_weather
# Create your views here.
def products_view(request):
    if request.method == "GET":
        # Обработка id из параметров запроса (уже было реализовано ранее)
        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"): # Если в параметрах есть 'ordering'
            if request.GET.get("reverse")  and request.GET.get("reverse").lower() == 'true': # Если в параметрах есть 'ordering' и 'reverse'=True
                # TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=True
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=True)
            else:  # Если не обнаружили в адресно строке ...&reverse=true , значит reverse=False
                # TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=False
                data = filtering_category(DATABASE, category_key, ordering_key, reverse=False)
        else:
            #  TODO Использовать filtering_category и провести фильтрацию с параметрами category
            data = filtering_category(DATABASE, category_key)
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                                 'indent': 4})
def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                # Если значение переданного параметра совпадает именем html файла
            # TODO 1. Откройте файл open(f'store/products/{page}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
                    with open(f'store/products/{page}.html', encoding="utf-8") as f:
                        fdata = f.read()
            # TODO 2. Прочитайте его содержимое
            # TODO 3. Верните HttpResponse c содержимым html файла
                        return HttpResponse(fdata)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(f'store/products/{data["html"]}.html',  encoding="utf-8") as f:
                    fdata = f.read()
                    return HttpResponse(fdata)
        # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
        # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        return HttpResponse(status=404)

def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ


def cart_view(request):
    if request.method == "GET":
        # TODO Вызвать ответственную за это действие функцию
        data = view_in_cart()
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


def cart_add_view(request, id_product):
    if request.method == "GET":
        # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        result = add_to_cart()
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        result = remove_from_cart()
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})