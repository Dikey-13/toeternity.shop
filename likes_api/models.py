# likes_api/models.py
from django.db import models
from django.utils import timezone # Додаємо для дати

# Ця модель у нас вже є
class Like(models.Model):
    item_id = models.CharField(max_length=100, primary_key=True)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.item_id}: {self.like_count}"

# ===== ДОДАЄМО НОВУ МОДЕЛЬ =====
class Artwork(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва роботи")
    description = models.TextField(verbose_name="Опис")
    # Зберігаємо зображення-прев'ю
    image_preview = models.ImageField(upload_to='art_previews/', verbose_name="Зображення-прев'ю")
    # Зберігаємо повне зображення для модального вікна
    image_full = models.ImageField(upload_to='art_full/', verbose_name="Повне зображення")
    # Дата створення, щоб знати, які роботи нові
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата додавання")
    # Посилання на інстаграм, якщо є
    instagram_link = models.URLField(max_length=250, blank=True, null=True, verbose_name="Посилання на Instagram")

    class Meta:
        # Сортування за замовчуванням: новіші роботи зверху
        ordering = ['-created_at']
        verbose_name = "Робота (Арт)"
        verbose_name_plural = "Роботи (Арти)"

    def __str__(self):
        return self.title