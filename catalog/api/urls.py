from django.urls import path
from . import views

urlpatterns = [
	path('authors/', views.author_list, name = 'api_authors_list'),
	path('author/<int:id>/', views.author_detail, name = 'api_author_detail'),
	path('books/', views.book_list, name = 'api_books_list'),
	path('book/<int:id>/', views.book_detail, name = 'api_book_detail'),
]