# likes_api/admin.py
from django.contrib import admin
from .models import Artwork, Like, Collection, ClothingItem, CollectionImage # Додаємо CollectionImage

# Inline-редактор для зображень колекції
# Це дозволить додавати зображення прямо на сторінці редагування колекції
class CollectionImageInline(admin.TabularInline):
    model = CollectionImage
    extra = 1 # Показує один порожній слот для завантаження нового зображення

# Оновлюємо адмін-клас для Collection, щоб він використовував inline-редактор
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    inlines = [CollectionImageInline, ] # Додаємо сюди наш inline-редактор

# Клас для ClothingItem залишається як був
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'gender', 'category', 'added_at')
    list_filter = ('collection', 'gender', 'category', 'added_at')
    search_fields = ('name', 'description', 'collection__name')

# Клас для Artwork залишається як був (або ваші налаштування для нього)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

# Реєструємо моделі
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Like)
admin.site.register(Collection, CollectionAdmin) # Реєструємо Collection з новими налаштуваннями
admin.site.register(ClothingItem, ClothingItemAdmin)
# Окремо реєструвати CollectionImage не потрібно, оскільки вона вже включена через inline