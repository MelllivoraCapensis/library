from django.urls import path
from . import views

urlpatterns = [
	path('authors/', views.AuthorCreateWithList.as_view(), name = 'authors_list'),
	path('author/<int:pk>/', views.AuthorDetail.as_view(), name = 'author_detail'),
	path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name = 'author_update'),
	path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name = 'author_delete'),

]