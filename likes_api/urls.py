# likes_api/urls.py
from django.urls import path
from . import views # Переконайтеся, що views імпортуються так

urlpatterns = [
    # Існуючі маршрути для лайків
    path('like/<str:item_id>', views.like_item, name='like_item'),
    path('unlike/<str:item_id>', views.unlike_item, name='unlike_item'),
    path('get_all_likes', views.get_all_likes, name='get_all_likes'),

    # Існуючий маршрут для деталей однієї колекції
    path('collection/<int:collection_pk>/', views.collection_detail_view, name='collection_detail'),

    # ===== НОВИЙ МАРШРУТ ДЛЯ СПИСКУ ВСІХ КОЛЕКЦІЙ =====
    # Цей маршрут буде вести на сторінку, де відображаються всі колекції.
    path('collections/', views.collections_list_view, name='collections_list'),
]