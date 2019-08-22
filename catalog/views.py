from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Author, Book, Reader
from django import forms

class AuthorCreateWithList(CreateView):
	model = Author
	fields = '__all__'

	success_url = './'

	def get_context_data(self, **kwargs):
		kwargs['authors'] = Author.objects.all()
		return super(CreateView, self).get_context_data(**kwargs)


class AuthorDetail(DetailView):
	model = Author

class AuthorUpdate(UpdateView):
	model = Author
	fields = '__all__'

class AuthorDelete(DeleteView):
	model = Author
	success_url = reverse_lazy('authors_list')

class BookCreateWithList(CreateView):
	model = Book
	fields = '__all__'
	success_url = './'

	def get_context_data(self, **kwargs):
		kwargs['books'] = Book.objects.all()
		return super(CreateView, self).get_context_data(**kwargs)

class BookDetail(DetailView):
	model = Book

class BookUpdate(UpdateView):
	model = Book
	fields = '__all__'

class BookDelete(DeleteView):
	model = Book
	success_url = reverse_lazy('books_list')

def reader_create_with_list(request):
	readers = Reader.objects.all()
	if request.method == 'POST':
		f = UserCreationForm(request.POST)
		if f.is_valid():
			new_user = f.save()
			readers_group = Group.objects.get(name = 'readers')
			new_user.groups.add(readers_group)
			new_user.save()
			Reader.objects.create(user = new_user)
			return redirect('login')
	else:
		f = UserCreationForm()
	return render(request, 'catalog/readers_list.html', {'form': f, 'readers': readers})

def reader_detail(request, id):
	reader = Reader.objects.get(id__exact = id)
	user_id = reader.user.id

	if request.method == 'POST':
		for item in dict(request.POST):
			if 'book_id_' in item:
				book = Book.objects.get(id__exact = item[8:])
				reader.books.add(book)

	reader_books = reader.books.all()
	reader_book_ids = list([book.id for book in reader_books])
	recommended_books = Book.objects.all().exclude(id__in = reader_book_ids)

	return render(request, 'catalog/reader_detail.html', 
		{'user_id': user_id, 'reader_books': reader_books, 
		'recommended_books': recommended_books, 'reader': reader})

def book_delete_from_reader_list(request, reader_id, book_id):
	reader = Reader.objects.get(id = reader_id)
	book_to_delete = Book.objects.get(id__exact = book_id)
	reader.books.remove(book_to_delete)
	return redirect(reader.get_absolute_url())