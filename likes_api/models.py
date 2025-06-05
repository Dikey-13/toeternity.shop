# likes_api/models.py
from django.db import models
from django.utils import timezone

# Ця модель у нас вже є
class Like(models.Model):
    item_id = models.CharField(max_length=100, primary_key=True)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.item_id}: {self.like_count}"

# Модель Artwork (перевірте, чи тут все гаразд з відступами у вашому оригіналі, тут я залишив як було у вас)
class Artwork(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва роботи")
    description = models.TextField(verbose_name="Опис")
    image_preview = models.ImageField(upload_to='art_previews/', verbose_name="Зображення-прев'ю")
    image_full = models.ImageField(upload_to='art_full/', verbose_name="Повне зображення")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата додавання")
    instagram_link = models.URLField(max_length=250, blank=True, null=True, verbose_name="Посилання на Instagram")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Робота (Арт)"
        verbose_name_plural = "Роботи (Арти)"

    def __str__(self):
        return self.title

# ===== НОВІ МОДЕЛІ ДЛЯ КОЛЕКЦІЙ ТА ПРЕДМЕТІВ ОДЯГУ (з правильними відступами) =====

class Collection(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Назва колекції")
    description = models.TextField(blank=True, verbose_name="Опис колекції")
    preview_image = models.ImageField(upload_to='collection_previews/', blank=True, null=True, verbose_name="Зображення-прев'ю колекції")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата створення")

    class Meta:
        ordering = ['-created_at'] # Новіші колекції зверху
        verbose_name = "Колекція одягу"
        verbose_name_plural = "Колекції одягу"

    def __str__(self):
        return self.name

class ClothingItem(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Чоловічий'),
        ('FEMALE', 'Жіночий'),
        ('UNISEX', 'Унісекс'),
    ]
    CATEGORY_CHOICES = [
        ('TOP', 'Верх (Top)'),
        ('BOTTOM', 'Низ (Bottom)'),
        ('SHOES', 'Взуття (Shoes)'),
        ('HAIR', 'Волосся (Hair)'),
        ('ACCESSORIES', 'Аксесуари (Accessories)'),
        ('FULL_OUTFIT', 'Повний образ (Full Outfit)'),
    ]

    collection = models.ForeignKey(Collection, related_name='items', on_delete=models.CASCADE, verbose_name="Належить до колекції")
    name = models.CharField(max_length=200, verbose_name="Назва предмету")
    description = models.TextField(blank=True, verbose_name="Опис предмету") 
    imvu_link = models.URLField(max_length=250, verbose_name="Посилання на IMVU")
    item_preview_image = models.ImageField(upload_to='clothing_items/', verbose_name="Зображення предмету")
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Стать")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Тип одягу")
    
    added_at = models.DateTimeField(default=timezone.now, verbose_name="Дата додавання")

    class Meta:
        ordering = ['-added_at'] # Новіші предмети зверху
        verbose_name = "Предмет одягу"
        verbose_name_plural = "Предмети одягу"

    def __str__(self):
        return f"{self.name} ({self.get_gender_display()} - {self.get_category_display()}) - з колекції '{self.collection.name}'"