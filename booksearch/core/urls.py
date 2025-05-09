from django.urls import path
from .views import (
    profile_view,
    books_list_view,
    user_books_list_view
)
urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('books/', books_list_view, name='books'),
    path('user_books/', user_books_list_view, name='user_books'),
]