from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.decorators import permission_required
from rest_framework import generics
from django.contrib.auth.mixins import PermissionRequiredMixin

@api_view(['GET', 'POST'])
def authors_list(request):
	if request.method == 'GET':
		authors = Author.objects.all()
		serializer = AuthorSerializer(authors, many = True)
		return Response(serializer.data)
	elif request.method == 'POST':
		if not request.user.has_perm('catalog.add_author'):
			return Response(data = 'У вас нет прав для данной операции', status = status.HTTP_403_FORBIDDEN)

		serializer = AuthorSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def author_detail(request, id):
	if request.method == 'GET':
		author = Author.objects.get(id__exact = id)
		serializer = AuthorSerializer(author)
		return Response(serializer.data)

	elif request.method == 'PUT' or request.method == 'PATCH':
		if not request.user.has_perm('catalog.change_author'):
			return Response(status = status.HTTP_403_FORBIDDEN)
		serializer = AuthorSerializer(author, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	
	elif request.method == 'DELETE':
		if not request.user.has_perm('catalog.delete_author'):
			return Response(status = status.HTTP_403_FORBIDDEN)
		author.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def books_list(request):
	if request.method == 'GET':
		books = Book.objects.all()
		serializer = BookSerializer(books, many = True)
		return Response(serializer.data)
	elif request.method == 'POST':
		if not request.user.has_perm('catalog.add_book'):
			return Response(data = 'У вас нет прав для данной операции', status = status.HTTP_403_FORBIDDEN)

		serializer = AuthorSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def book_detail(request, id):
	if request.method == 'GET':
		book = Book.objects.get(id__exact = id)
		serializer = BookSerializer(book)
		return Response(serializer.data)

	elif request.method == 'PUT' or request.method == 'PATCH':
		if not request.user.has_perm('catalog.change_book'):
			return Response(status = status.HTTP_403_FORBIDDEN)
		serializer = BookSerializer(book, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
	
	elif request.method == 'DELETE':
		if not request.user.has_perm('catalog.delete_book'):
			return Response(status = status.HTTP_403_FORBIDDEN)
		book.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)



