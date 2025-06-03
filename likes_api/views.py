from django.shortcuts import render

# Create your views here.

# likes_api/views.py

from django.shortcuts import render # Важливо: імпортуємо render для роботи з шаблонами
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from .models import Like, Artwork # Тепер імпортуємо і Artwork

# ===============================================
# ===== НОВІ VIEWS ДЛЯ ВІДОБРАЖЕННЯ РОБІТ =====
# ===============================================

def index_page(request):
    """
    Ця view відповідає за головну сторінку.
    """
    # 1. Беремо з бази даних 3 останні роботи, сортуючи їх за датою (новіші перші)
    latest_artworks = Artwork.objects.order_by('-created_at')[:3]
    
    # 2. Створюємо "контекст" - словник з даними, які ми передамо в HTML
    context = {
        'artworks': latest_artworks
    }
    
    # 3. "Рендеримо" шаблон index.html, передаючи в нього наш контекст
    return render(request, 'index.html', context)

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