from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Author, Book, Reader
from django.contrib.auth.models import User
from .serializers import AuthorSerializer, BookSerializer, ReaderSerializer
from rest_framework import status


@api_view(['GET', 'POST'])
def author_list(request):
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


@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, id):
	author = Author.objects.get(id = id)
	if request.method == 'GET':
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
def book_list(request):

	if request.method == 'GET':
		books = Book.objects.all()
		serializer = BookSerializer(books, many = True)
		return Response(serializer.data)
		
	elif request.method == 'POST':
		if not request.user.has_perm('catalog.add_book'):
			return Response(data = 'У вас нет прав для данной операции', status = status.HTTP_403_FORBIDDEN)

		serializer = BookSerializer(data = request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, id):
	book = Book.objects.get(id = id)
	if request.method == 'GET':
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


@api_view(['GET'])
def reader_list(request):
	readers = Reader.objects.all()
	serializer = ReaderSerializer(readers, many = True)
	return Response(serializer.data)

@api_view(['GET'])
def reader_books(request, id):
	reader_books = Reader.objects.get(id = id).books.all()
	serializer = BookSerializer(reader_books, many = True)
	return Response(serializer.data)

@api_view(['GET'])
def author_books(request, id):
	author_books = Author.objects.get(id = id).book_set.all()
	serializer = BookSerializer(author_books, many = True)
	return Response(serializer.data)
