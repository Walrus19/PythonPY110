import json
import os
from itertools import product
from django.contrib.auth import get_user
from urllib3 import request

from store.models import DATABASE
from django.contrib.auth import login, authenticate, get_user


def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False) -> list[dict]:
    """
    Функция фильтрации данных по параметрам

    :param database: База данных. (словарь словарей. При проверке в качестве database будет передаваться словарь DATABASE из models.py)
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    if category_key is not None:
        # TODO При помощи фильтрации в list comprehension профильтруйте товары по категории (ключ 'category') в продукте database. Или можете использовать
        result = [product for product in database.values() if product['category'] == category_key]
        print(result)
        # обычный цикл или функцию filter. Допустим фильтрацию в list comprehension можно сделать по следующему шаблону
        # [product for product in database.values() if ...] подумать, что за фильтрующее условие можно применить.
        # Сравните значение категории продукта со значением category_key
    else:
        result = list(database.values())
        # TODO Трансформируйте словарь словарей database в список словарей
        # В итоге должен быть [dict, dict, dict, ...], где dict - словарь продукта из database
    if ordering_key is not None:
        ...  # TODO Проведите сортировку result по ordering_key и параметру reverse
        result.sort(key=lambda item:item[ordering_key], reverse=reverse)
        # Так как result будет списком, то можно применить метод sort, но нужно определиться с тем по какому элементу сортируем и в каком направлении
        # result.sort(key=lambda ..., reverse=reverse)
        # Вспомните как можно сортировать по значениям словаря при помощи lambda функции
    return result



def view_in_cart(request) -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username  # Получаем авторизированного пользователя
    cart = {user: {'products': {}}}  # создаем пустую корзину.
    with open('cart.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    # TODO Помните, что у вас есть уже реализация просмотра корзины,
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if id_product not in cart['products']:
        if not DATABASE.get(id_product):
            return False
        cart['products'][id_product] = 1
    else:
        cart['products'][id_product] += 1

    with open('cart.json', mode='w', encoding='utf-8') as f:  # Создаём файл и записываем туда текущую корзину
        json.dump(cart_users, f)

    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # ! Обратите внимание, что в переменной cart находится словарь с ключом products.
    # ! Именно в cart["products"] лежит словарь гдк по id продуктов можно получить число продуктов в корзине.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной cart нужно вызвать
    # ! cart["products"][id_product]
    # ! Далее уже сами решайте как и в какой последовательности дальше действовать.

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то перед тем как его добавить - проверьте есть ли такой id_product товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.
    # if DATABASE.get(id_product):
    #     # TODO Если товар существует, то увеличиваем его количество на 1
    #     cart["products"][id_product] =count + 1
    # TODO Не забываем записать обновленные данные cart в 'cart.json'. Так как именно из этого файла мы считываем данные и если мы не запишем изменения, то считать измененные данные не получится.

    return True


def remove_from_cart(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    # TODO Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]
    # С переменной cart функции remove_from_cart ситуация аналогичная, что с cart функции add_to_cart

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.
    if id_product not in cart['products']:
        return False
    # TODO Если существует товар, то удаляем ключ 'id_product' у cart['products'].
    else:
        cart['products'].pop(id_product)
    # TODO Не забываем записать обновленные данные cart в 'cart.json'
    with open('cart.json', mode='w', encoding='utf-8') as f:  # Создаём файл и записываем туда текущую корзину
        json.dump(cart_users, f)
    return True

def add_user_to_cart(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных корзины, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    cart_users = view_in_cart(request)  # Чтение всей базы корзин

    cart = cart_users.get(username)  # Получение корзины конкретного пользователя

    if not cart:  # Если пользователя до настоящего момента не было в корзине, то создаём его и записываем в базу
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)

def view_in_wishlist(request) -> dict:
    """
      Просматривает содержимое wishlist.json

      :return: Содержимое 'wishlist.json'
      """
    if os.path.exists('wishlist.json'):  # Если файл существует
        with open('wishlist.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username  # Получаем авторизированного пользователя
    wishlist = {user: {'products': []}}  # создаем пустое избранное.
    with open('wishlist.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустое избранное
        json.dump(wishlist, f)

    return wishlist

def add_to_wishlist(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    # TODO Помните, что у вас есть уже реализация просмотра избранного,
    wishlist_users = view_in_wishlist(request)
    wishlist= wishlist_users[get_user(request).username]

    if id_product not in wishlist['products']:
        if DATABASE.get(id_product):
            wishlist['products'].append(id_product)
        else:
            return False


    with open('wishlist.json', mode='w', encoding='utf-8') as f:  # Создаём файл и записываем туда текущую корзину
        json.dump(wishlist_users, f)

    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # ! Обратите внимание, что в переменной cart находится словарь с ключом products.
    # ! Именно в cart["products"] лежит словарь гдк по id продуктов можно получить число продуктов в корзине.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной cart нужно вызвать
    # ! cart["products"][id_product]
    # ! Далее уже сами решайте как и в какой последовательности дальше действовать.

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то перед тем как его добавить - проверьте есть ли такой id_product товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.
    # if DATABASE.get(id_product):
    #     # TODO Если товар существует, то увеличиваем его количество на 1
    #     cart["products"][id_product] =count + 1
    # TODO Не забываем записать обновленные данные cart в 'cart.json'. Так как именно из этого файла мы считываем данные и если мы не запишем изменения, то считать измененные данные не получится.

    return True

def remove_from_wishlist(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    # TODO Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]
    # С переменной cart функции remove_from_cart ситуация аналогичная, что с cart функции add_to_cart

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.
    if id_product not in wishlist['products']:
        return False
    # TODO Если существует товар, то удаляем ключ 'id_product' у cart['products'].
    else:
        wishlist['products'].remove(id_product)
    # TODO Не забываем записать обновленные данные cart в 'cart.json'
    with open('wishlist.json', mode='w', encoding='utf-8') as f:  # Создаём файл и записываем туда текущую корзину
        json.dump(wishlist_users, f)
    return True

def add_user_to_wishlist(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных корзины, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    wishlist_users = view_in_wishlist(request)  # Чтение всей базы корзин

    wishlist = wishlist_users.get(username)  # Получение корзины конкретного пользователя

    if not wishlist:  # Если пользователя до настоящего момента не было в корзине, то создаём его и записываем в базу
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            wishlist_users[username] = {'products': []}
            json.dump(wishlist_users, f)

if __name__ == "__main__":
    # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
    # Для совпадения выходных значений перед запуском скрипта удаляйте появляющийся файл 'cart.json' в папке
    print(view_in_cart(request))  # {'products': {}}
    print(add_to_cart('1'))  # True
    print(add_to_cart('0'))  # False
    print(add_to_cart('1'))  # True
    print(add_to_cart('2'))  # True
    print(view_in_cart())  # {'products': {'1': 2, '2': 1}}
    print(remove_from_cart('0'))  # False
    print(remove_from_cart('1'))  # True
    print(view_in_cart())  # {'products': {'2': 1}}

    # Предыдущий код, что был для проверки filtering_category закомментируйте

# if __name__ == "__main__":
#     from store.models import DATABASE
#
#     test = [
#         {'name': 'Клубника', 'discount': None, 'price_before': 500.0,
#          'price_after': 500.0,
#          'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
#          'rating': 5.0, 'review': 200, 'sold_value': 700,
#          'weight_in_stock': 400,
#          'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg',
#          'html': 'strawberry'},
#
#         {'name': 'Яблоки', 'discount': None, 'price_before': 130.0,
#          'price_after': 130.0,
#          'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
#          'rating': 4.7, 'review': 30, 'sold_value': 70, 'weight_in_stock': 200,
#          'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg',
#          'html': 'apple'}
#     ]
#
#     print(filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True








