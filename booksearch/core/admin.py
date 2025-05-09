from django.contrib import admin

from .models import Category, Book, Profile, FavoriteBook

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(FavoriteBook)
