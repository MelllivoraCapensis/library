from django.contrib import admin
from .models import Author, Book, Reader

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 
		'date_of_birth', 'date_of_death')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'year', 'description')

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
	fields = ['user', 'books']
	list_display = ('user', 'get_books')