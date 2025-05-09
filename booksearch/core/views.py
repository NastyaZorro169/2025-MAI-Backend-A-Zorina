from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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
            "books": [
                {"id": 1, "title": "Python Basics", "author": "John Smith"},
                {"id": 2, "title": "Learning Django", "author": "Jane Doe"},
                {"id": 3, "title": "Advanced Python", "author": "Alice Johnson"}]
        })
    elif request.method == 'POST':
        return JsonResponse({"status": "books updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
@csrf_exempt
def user_books_list_view(request):
    if request.method == 'GET':
        return JsonResponse({
            "user_books": [
                {"id": 1, "id_user": 1, "title": "Python Basics", "author": "John Smith"},
                {"id": 2, "id_user": 1, "title": "Learning Django", "author": "Jane Doe"}
            ]
        })
    elif request.method == 'POST':
        return JsonResponse({"users_books": "users_books updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

