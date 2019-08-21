from django.urls import path
from . import views

urlpatterns = [
	path('authors/', views.AuthorCreateWithList.as_view(), name = 'authors_list'),
	path('author/<int:pk>/', views.AuthorDetail.as_view(), name = 'author_detail'),
	path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name = 'author_update'),
	path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name = 'author_delete'),
	path('books/', views.BookCreateWithList.as_view(), name = 'books_list'),
	path('book/<int:pk>/', views.BookDetail.as_view(), name = 'book_detail'),
	path('book/<int:pk>/update/', views.BookUpdate.as_view(), name = 'book_update'),
	path('book/<int:pk>/delete/', views.BookDelete.as_view(), name = 'book_delete'),
	path('readers/', views.reader_create_with_list, name = 'readers_list'),
	# path('user/<int:id>/books/', views.books_list_by_user, name = 'book_list_by_user'),
]