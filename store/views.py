from django.db.models.expressions import result
from django.contrib.auth.decorators import login_required
from logic.services import filtering_category
from django.shortcuts import render
from django.http import JsonResponse
from store.models import DATABASE
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from django.shortcuts import redirect
from django.contrib.auth import get_user
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
            if request.GET.get("reverse") and request.GET.get("reverse").lower() == 'true': # Если в параметрах есть 'ordering' и 'reverse'=True
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
# def products_page_view(request, page):
#     if request.method == "GET":
#         if isinstance(page, str):
#             for data in DATABASE.values():
#                 if data['html'] == page:
#                 # Если значение переданного параметра совпадает именем html файла
#             # TODO 1. Откройте файл open(f'store/products/{page}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
#                     with open(f'store/products/{page}.html', encoding="utf-8") as f:
#                         fdata = f.read()
#             # TODO 2. Прочитайте его содержимое
#             # TODO 3. Верните HttpResponse c содержимым html файла
#                         return HttpResponse(fdata)
#         elif isinstance(page, int):
#             data = DATABASE.get(str(page))
#             if data:
#                 with open(f'store/products/{data["html"]}.html',  encoding="utf-8") as f:
#                     fdata = f.read()
#                     return HttpResponse(fdata)
#         # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
#         # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
#         return HttpResponse(status=404)

def products_page_view(request, page):
    if request.method == "GET":
        data_product = None

        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    data_product = data
                    break
        if data_product:
            data1 = [prod for prod in filtering_category(DATABASE, data_product['category']) if prod['id'] != data_product['id']]
            return render(request, "store/product.html", context={"product": data_product, "products": data1})

        elif isinstance(page, int):
            # Обрабатываем условие того, что пытаемся получить страницу товара по его id
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:
                return render(request, "store/product.html", context={"product": data, "products": data1})

        return HttpResponse(status=404)

def shop_view(request):
    if request.method == "GET":
        # with open('store/shop.html', encoding="utf-8") as f:
        #     data = f.read()  # Читаем HTML файл
        # return HttpResponse(data)  # Отправляем HTML файл как ответ
        # return render(request, 'store/shop.html', context={"products": DATABASE.values()})
        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
             if request.GET.get("reverse") in ('true', 'True'):
                 data = filtering_category(DATABASE, category_key, ordering_key,True)
             else:
                 data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return render(request, 'store/shop.html', context={"products": data, "category": category_key})

@login_required(login_url='login:login_view')
def cart_view(request):
    if request.method == "GET":
        # # TODO Вызвать ответственную за это действие функцию
        # data = view_in_cart()
        # return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
        #                                              'indent': 4})
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]

        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            # 1. Получите информацию о продукте из DATABASE по его product_id. product будет словарём
            product = DATABASE.get(product_id)
            # product = product_id['description']
            # 2. в словарь product под ключом "quantity" запишите текущее значение товара в корзине
            product["quantity"] = quantity
            product["price_total"] = f"{quantity * product['price_after']:.2f}"  # добавление общей цены позиции с ограничением в 2 знака
            # 3. добавьте product в список products
            products.append(product)
            # cart_add_view(request, product_id)
        return render(request, "store/cart.html", context={"products": products})

@login_required(login_url='login:login_view')
def cart_add_view(request, id_product):
    if request.method == "GET":
        # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        result = add_to_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def cart_del_view(request, id_product):
    if request.method == "GET":
        # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        result = remove_from_cart(id_product)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def coupon_check_view(request, coupon):
    # DATA_COUPON - база данных купонов: ключ - код купона (name_coupon); значение - словарь со значением скидки в процентах и
    # значением действителен ли купон или нет
    DATA_COUPON = {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
    }
    if request.method == "GET":
        # TODO Проверьте, что купон есть в DATA_COUPON, если он есть, то верните JsonResponse в котором по ключу "discount"
        # получают значение скидки в процентах, а по ключу "is_valid" понимают действителен ли купон или нет (True, False)

        # TODO Если купона нет в базе, то верните HttpResponseNotFound("Неверный купон")
            result = DATA_COUPON.get(coupon)
            if result:
                return JsonResponse( {"discount": result.get("value"), "is_valid": result.get("is_valid")}, json_dumps_params={'ensure_ascii': False,
                                                           'indent': 4})
            else:
                return HttpResponseNotFound("Неверный купон")

def delivery_estimate_view(request):
    # База данных по стоимости доставки. Ключ - Страна; Значение словарь с городами и ценами; Значение с ключом fix_price
    # применяется если нет города в данной стране
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 90},
            "fix_price": 100,
        },
    }
    if request.method == "GET":
        data = request.GET
        country = data.get('country')
        city = data.get('city')
        # TODO Реализуйте логику расчёта стоимости доставки, которая выполняет следующее:
        # Если в базе DATA_PRICE есть и страна (country) и существует город(city), то вернуть JsonResponse со словарём, {"price": значение стоимости доставки}
        # Если в базе DATA_PRICE есть страна, но нет города, то вернуть JsonResponse со словарём, {"price": значение фиксированной стоимости доставки}
        # Если нет страны, то вернуть HttpResponseNotFound("Неверные данные")
        if country in DATA_PRICE and city in DATA_PRICE[country]:
            return JsonResponse({"price": DATA_PRICE[country][city]["price"]},
                                json_dumps_params={'ensure_ascii': False,
                                                   'indent': 4})
        elif country in DATA_PRICE and city is None:
            return JsonResponse({"price": DATA_PRICE[country]["fix_price"]},
                                json_dumps_params={'ensure_ascii': False,
                                                   'indent': 4})
        else:
            return HttpResponseNotFound("Неверные данные")
@login_required(login_url='login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound("Неудачное добавление в корзину")

def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)  # TODO Вызвать функцию удаления из корзины
        if result:
            return redirect("store:cart_view")  # TODO Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из корзины")