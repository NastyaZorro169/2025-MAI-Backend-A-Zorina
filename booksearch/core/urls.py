from django.urls import path
from .views import (
    profile_create_view,
    profile_detail_view,
    books_list_view,
    books_create_view,
    user_books_list_view,
    user_books_add_view,
    books_by_category_view,
    categories_list_view,
    search_view
)
urlpatterns = [
    # Профиль: создание (POST) и просмотр (GET по user_id)
    path('profile/create/', profile_create_view, name='profile_create'),
    path('profile/<int:user_id>/', profile_detail_view, name='profile_detail'),

    # Книги: список и создание
    path('books/', books_list_view, name='books_list'),
    path('books/create/', books_create_view, name='books_create'),

    # Любимые книги пользователя: список и добавление
    path('user_books/', user_books_list_view, name='user_books_list'),
    path('user_books/add/', user_books_add_view, name='user_books_add'),

    # Категории книг
    path('categories/', categories_list_view, name='categories_list'),

    # Книги по категории
    path('categories/<str:category_name>/', books_by_category_view, name='books_by_category'),

    # Поиск книг
    path('search/', search_view, name='search'),
]