from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q

import json

from core.models import Book, Category, Profile, FavoriteBook


@csrf_exempt
@require_http_methods(["POST"])
def profile_create_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'student')

        if not username or not password:
            return JsonResponse({"error": "username and password are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "User with this username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role=role)

        return JsonResponse({"status": "User created", "user_id": user.id}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
        

@csrf_exempt
@require_http_methods(["GET"])
def profile_detail_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        profile = user.profile  # assuming OneToOne relation Profile
        return JsonResponse({
            "username": user.username,
            "role": profile.role
        })
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    
# показать все книги
@csrf_exempt
@require_http_methods(["GET"])
def books_list_view(request):
    books = Book.objects.all()
    results = []
    for book in books:
        results.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category.name
        })
    return JsonResponse({"books": results})

# создать книгу 
@csrf_exempt
@require_http_methods(["POST"])
def books_create_view(request):
    try:
        data = json.loads(request.body)
        title = data.get('title')
        author = data.get('author')
        category_name = data.get('category')

        if not all([title, author, category_name]):
            return JsonResponse({"error": "Поля title, author и category обязательны"}, status=400)

        category, created = Category.objects.get_or_create(name=category_name)

        book = Book.objects.create(title=title, author=author, category=category)

        return JsonResponse({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category.name
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Неверный формат JSON"}, status=400)
    

# показать все любимые книги пользователя  
@csrf_exempt
@require_http_methods(["GET"])
def user_books_list_view(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({"error": "user_id parameter is required"}, status=400)
    try:
        user_id = int(user_id)
    except ValueError:
        return JsonResponse({"error": "user_id must be an integer"}, status=400)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    favorites = FavoriteBook.objects.filter(user=user).select_related('book', 'book__category')
    books = [{
        "id": fav.book.id,
        "title": fav.book.title,
        "author": fav.book.author,
        "category": fav.book.category.name
    } for fav in favorites]

    return JsonResponse({"users_books": books})


 # добавить любимую книгу   
@csrf_exempt
@require_http_methods(["POST"])
def user_books_add_view(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({"error": "user_id parameter is required in query string"}, status=400)
    try:
        user_id = int(user_id)
    except ValueError:
        return JsonResponse({"error": "user_id must be an integer"}, status=400)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
        if not book_id:
            return JsonResponse({"error": "book_id is required in request body"}, status=400)
        book = Book.objects.get(pk=book_id)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    favorite, created = FavoriteBook.objects.get_or_create(user=user, book=book)
    if created:
        return JsonResponse({"status": "Book added to favorites"})
    else:
        return JsonResponse({"status": "Book already in favorites"})
    
    

# показать все категории 
@csrf_exempt
@require_http_methods(["GET"])
def categories_list_view(request):
    categories = Category.objects.all()
    categories_list = [{"id": cat.id, "name": cat.name} for cat in categories]
    return JsonResponse({"categories": categories_list})

    
# поиск книги 
@csrf_exempt
@require_http_methods(["GET"])
def search_view(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({"error": "Параметр q обязателен"}, status=400)

    books = Book.objects.filter(
        Q(title__icontains=q) | Q(author__icontains=q)
    )

    results = []
    for book in books:
        results.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": book.category.name
        })

    return JsonResponse({"results": results})

@csrf_exempt
@require_http_methods(["GET"])
def books_by_category_view(request, category_name):
    try:
        category = Category.objects.get(name__iexact=category_name)
    except Category.DoesNotExist:
        return JsonResponse({"message": "ничего не найдено"}, status=404)

    books = Book.objects.filter(category=category)
    if not books.exists():
        return JsonResponse({"message": "ничего не найдено"})

    results = []
    for book in books:
        results.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "category": category.name
        })

    return JsonResponse({"books": results})

