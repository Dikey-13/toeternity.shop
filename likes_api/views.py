from django.shortcuts import render

# Create your views here.

# likes_api/views.py
from django.shortcuts import render, get_object_or_404 # Додайте get_object_or_404, якщо його немає
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from .models import Like, Artwork, Collection, ClothingItem # Додайте Collection та ClothingItem

# ===============================================
# ===== НОВІ VIEWS ДЛЯ ВІДОБРАЖЕННЯ РОБІТ =====
# ===============================================

def index_page(request):
    """
    Ця view відповідає за головну сторінку.
    """
    latest_artworks = Artwork.objects.order_by('-created_at')[:3]
    latest_collections = Collection.objects.order_by('-created_at')[:3]
    
    context = {
        'artworks': latest_artworks,
        'collections_list_on_home': latest_collections,
    }
    
    return render(request, 'index.html', context) # <-- ОСЬ ЦЕЙ РЯДОК БУВ ПРОПУЩЕНИЙ


def gallery_page(request):
    """
    Ця view відповідає за нову сторінку галереї.
    """
    # 1. Беремо з бази даних АБСОЛЮТНО ВСІ роботи.
    # Сортування вже задане за замовчуванням у самій моделі.
    all_artworks = Artwork.objects.all()
    
    context = {
        'artworks': all_artworks
    }
    
    # 2. Рендеримо НОВИЙ шаблон gallery.html, який ми створимо на наступному кроці
    return render(request, 'gallery.html', context)

def collection_detail_view(request, collection_pk):
    """
    Відображає детальну інформацію про одну колекцію та предмети одягу в ній.
    'collection_pk' - це Primary Key (ID) колекції, який ми передамо через URL.
    """
    # 1. Отримуємо об'єкт колекції з бази даних за її ID (pk).
    # Функція get_object_or_404 дуже зручна: якщо об'єкт з таким pk
    # не знайдено, вона автоматично поверне сторінку з помилкою 404 (Not Found).
    collection_obj = get_object_or_404(Collection, pk=collection_pk)

    # 2. Отримуємо всі предмети одягу (ClothingItem), що належать до цієї конкретної колекції.
    # Ми використовуємо 'items' - це related_name, який ми вказали у полі 'collection'
    # моделі ClothingItem (collection = models.ForeignKey(Collection, related_name='items', ...)).
    # .all() поверне всі пов'язані об'єкти. Сортування буде таким,
    # як вказано в Meta класі моделі ClothingItem (за 'added_at').
    clothing_items_in_collection = collection_obj.items.all() 

    # 3. Створюємо словник 'context' з даними, які ми хочемо передати в HTML-шаблон.
    context = {
        'collection': collection_obj,  # Передаємо сам об'єкт колекції
        'clothing_items': clothing_items_in_collection, # Передаємо список предметів одягу
    }

    # 4. "Рендеримо" (відображаємо) новий HTML-шаблон з назвою 'collection_detail.html',
    # передаючи в нього наш словник 'context'.
    # Цей HTML-шаблон ми створимо на наступному кроці.
    return render(request, 'collection_detail.html', context)

# =========================================================
# ===== СТАРІ VIEWS ДЛЯ ЛАЙКІВ (залишаються без змін) =====
# =========================================================

@csrf_exempt
@require_POST
def like_item(request, item_id):
    obj, created = Like.objects.get_or_create(item_id=item_id)
    obj.like_count = F('like_count') + 1
    obj.save()
    obj.refresh_from_db()
    return JsonResponse({
        'success': True,
        'message': f"Лайк для {item_id} додано.",
        'current_likes_on_server': obj.like_count
    })

@csrf_exempt
@require_POST
def unlike_item(request, item_id):
    obj, created = Like.objects.get_or_create(item_id=item_id)
    if not created and obj.like_count > 0:
        obj.like_count = F('like_count') - 1
        obj.save()
        obj.refresh_from_db()
    return JsonResponse({
        'success': True,
        'message': f"Лайк для {item_id} знято.",
        'current_likes_on_server': obj.like_count
    })

def get_all_likes(request):
    all_likes = Like.objects.all()
    likes_data = {like.item_id: like.like_count for like in all_likes}
    return JsonResponse({
        'success': True,
        'message': "Лайки успішно завантажені.",
        'likes': likes_data
    })

def collections_list_view(request):
    """
    Відображає сторінку зі списком усіх колекцій.
    """
    all_collections = Collection.objects.all()
    print(f"--- DEBUG: Inside collections_list_view ---") # Діагностичний print
    print(f"QuerySet all_collections from view: {all_collections}") # Діагностичний print
    for c_debug in all_collections: # Діагностичний print
        print(f"Found in view: ID={c_debug.id}, Name='{c_debug.name}', Items: {c_debug.items.count()}") # Діагностичний print

    context = {
        'collections_list': all_collections,
    }
    print(f"Context being passed to template: {context}") # Діагностичний print

    return render(request, 'collections_list.html', context)