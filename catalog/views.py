from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from .models import Author, Book

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