# likes_api/admin.py
from django.contrib import admin
from .models import Artwork, Like, Collection, ClothingItem # Додаємо Collection та ClothingItem

# Кастомізація відображення Artwork в адмінці
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at') # Які поля показувати у списку
    search_fields = ('title', 'description') # За якими полями можна шукати
    list_filter = ('created_at',) # Фільтр за датою

# Кастомізація відображення Collection в адмінці
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

# Кастомізація відображення ClothingItem в адмінці
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'gender', 'category', 'added_at')
    list_filter = ('collection', 'gender', 'category', 'added_at') # Додаємо фільтри
    search_fields = ('name', 'description', 'collection__name') # Можна шукати за назвою колекції

# Реєструємо моделі
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Like) # Для Like поки проста реєстрація
admin.site.register(Collection, CollectionAdmin)
admin.site.register(ClothingItem, ClothingItemAdmin)