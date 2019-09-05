from django.urls import path
from . import views

urlpatterns = [
	path('authors/', views.AuthorList.as_view(), name = 'authors_list'),
	path('author/<int:pk>/', views.AuthorDetail.as_view(), name = 'author_detail'),
	path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name = 'author_update'),
	path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name = 'author_delete'),
	path('books/', views.BookList.as_view(), name = 'books_list'),
	path('book/<int:pk>/', views.BookDetail.as_view(), name = 'book_detail'),
	path('book/<int:pk>/update/', views.BookUpdate.as_view(), name = 'book_update'),
	path('book/<int:pk>/delete/', views.BookDelete.as_view(), name = 'book_delete'),
	path('readers/', views.reader_create_with_list, name = 'readers_list'),
	path('reader/<int:id>/books/', views.reader_book_list, name = 'reader_book_list'),
	path('reader/<int:id>/grades/', views.GradesListByReader.as_view(), name = 'reader_grade_list'),
	path('reader/<int:reader_id>/book/<int:book_id>/delete/',
		views.book_delete_from_reader_list, name = 'book_delete_from_reader_list'),
	path('reader/<int:reader_id>/book/<int:book_id>/add/',
		views.book_add_to_reader_list, name = 'book_add_to_reader_list'),
	path('reader/<int:pk>/image/update/', views.ReaderUpdate.as_view(), name = 'reader_update'),
]