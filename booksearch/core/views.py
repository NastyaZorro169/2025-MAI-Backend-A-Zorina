from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

BOOKS = [
    {"id": 1, "title": "Python Basics", "author": "John Smith", "category": "Programming"},
    {"id": 2, "title": "Learning Django", "author": "Jane Doe", "category": "Web Development"},
    {"id": 3, "title": "Advanced Python", "author": "Alice Johnson", "category": "Programming"},
    {"id": 4, "title": "Algebra 101", "author": "Bob Brown", "category": "Science"},
]
@csrf_exempt
def profile_view(request):
    if request.method == 'GET':
        return JsonResponse({"id": 1, "username": "john_doe", "role": "student", "books_count": 2})
    elif request.method == 'POST':
        return JsonResponse({"status": "profile updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
@csrf_exempt
def books_list_view(request):
    if request.method == 'GET':
        return JsonResponse({
            BOOKS
        })
    elif request.method == 'POST':
        return JsonResponse({"status": "books updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
@csrf_exempt
def user_books_list_view(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({"error": "user_id parameter is required"}, status=400)
        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({"error": "user_id must be an integer"}, status=400)

        return JsonResponse({
            "users_books": [
                {"id": 1, "id_user": 1, "title": "Python Basics", "author": "John Smith","category": "Programming"},
                {"id": 2, "id_user": 1, "title": "Learning Django", "author": "Jane Doe", "category": "Web Development"}
            ]
        })
        

    elif request.method == 'POST':
        # Для примера просто возвращаем статус
        return JsonResponse({"users_books": "users_books updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
@csrf_exempt
def books_by_category_view(request, category_name):
    if request.method == 'GET':
        # Фильтруем книги по категории (без учёта регистра)
        filtered_books = [book for book in BOOKS if book['category'].lower() == category_name.lower()]
        if filtered_books:
            return JsonResponse({"books": filtered_books})
        else:
            return JsonResponse({"message": "ничего не найдено"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    

@csrf_exempt
def categories_list_view(request):
    if request.method == 'GET':
        return JsonResponse({
            "categories": [
                {"id": 1, "name": "Programming"},
                {"id": 2, "name": "Web Development"},
                {"id": 3, "name": "Mathematics"},
                {"id": 4, "name": "Science"}
            ]
        })
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

