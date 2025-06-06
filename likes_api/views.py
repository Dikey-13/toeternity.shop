# likes_api/views.py

# Основні імпорти Django, які нам потрібні
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

# Імпортуємо всі наші моделі
from .models import Like, Artwork, Collection, ClothingItem

# ===============================================
# ===== VIEWS ДЛЯ ОСНОВНИХ СТОРІНОК САЙТУ =====
# ===============================================

def index_page(request):
    """
    Ця view відповідає за головну сторінку.
    """
    latest_artworks = Artwork.objects.order_by('-created_at')[:3]

    # Оновлений запит для колекцій
    latest_collections = Collection.objects.order_by('-created_at').prefetch_related('items')[:3]

    context = {
        'artworks': latest_artworks,
        'collections_list_on_home': latest_collections,
    }

    return render(request, 'index.html', context)
    
    # Створюємо контекст з даними для передачі в шаблон 'index.html'
    context = {
        'artworks': latest_artworks,
        'collections_list_on_home': latest_collections,
    }
    
    return render(request, 'index.html', context)


def gallery_page(request):
    """
    Відображає сторінку галереї з усіма роботами (Артами).
    """
    all_artworks = Artwork.objects.all() # .all() використовує сортування з Meta-класу моделі
    
    context = {
        'artworks': all_artworks
    }
    
    return render(request, 'gallery.html', context)


# =============================================================
# ===== VIEWS ДЛЯ СТОРІНОК СПИСКУ ТА ДЕТАЛЕЙ КОЛЕКЦІЙ =====
# =============================================================

def collections_list_view(request):
    """
    Відображає сторінку зі списком усіх колекцій.
    """
    all_collections = Collection.objects.all()
    
    context = {
        'collections_list': all_collections,
    }
    
    return render(request, 'collections_list.html', context)


def collection_detail_view(request, collection_pk):
    """
    Відображає детальну інформацію про одну колекцію,
    включаючи її галерею зображень та список предметів одягу.
    """
    collection_obj = get_object_or_404(Collection, pk=collection_pk)
    collection_images = collection_obj.images.all() # Використовує related_name='images'
    clothing_items_in_collection = collection_obj.items.all() # Використовує related_name='items'

    context = {
        'collection': collection_obj,
        'collection_images': collection_images,
        'clothing_items': clothing_items_in_collection,
    }
    
    return render(request, 'collection_detail.html', context)


# =========================================================
# ===== API VIEWS ДЛЯ СИСТЕМИ ЛАЙКІВ (без змін) =====
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
