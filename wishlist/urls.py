from django.urls import path
from .views import wishlist_view
#  TODO Импортируйте ваше представление

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name="wishlist_view"),  # TODO Зарегистрируйте обработчик

]