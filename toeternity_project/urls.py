# toeternity_project/urls.py

from django.contrib import admin
from django.urls import path, include
# from django.views.generic import TemplateView  # Цей рядок більше не потрібен, видаляємо

from likes_api import views as likes_api_views  # Імпортуємо наші views з додатку

# Додаємо імпорти для роботи з медіафайлами
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('likes_api.urls')),

    # Змінюємо: тепер головна сторінка ('') обслуговується нашою функцією index_page
    path('', likes_api_views.index_page, name='home'),

    # Додаємо новий маршрут для сторінки галереї
    path('gallery/', likes_api_views.gallery_page, name='gallery'),
]

# Додаємо цей рядок, щоб Django міг показувати завантажені зображення в режимі розробки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)