from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 
		'date_of_birth', 'date_of_death')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'year', 'description')
