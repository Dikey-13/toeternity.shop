# likes_api/admin.py
from django.contrib import admin
from .models import Artwork, Like # Імпортуємо наші моделі

# Реєструємо моделі, щоб вони з'явились в адмін-панелі
admin.site.register(Artwork)
admin.site.register(Like)