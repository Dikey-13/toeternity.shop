# likes_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('like/<str:item_id>', views.like_item, name='like_item'),
    path('unlike/<str:item_id>', views.unlike_item, name='unlike_item'),
    path('get_all_likes', views.get_all_likes, name='get_all_likes'),
]