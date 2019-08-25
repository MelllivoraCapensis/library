from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Author, Book, Reader
from django import forms
from .forms import AuthorForm, BookForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class AuthorList(ListView):
	model = Author

	def get_context_data(self, **kwargs):
		if self.request.user.has_perm('catalog.add_author'):
			kwargs['form'] = AuthorForm()
		return super(ListView, self).get_context_data(**kwargs)

class AuthorDetail(DetailView):
	model = Author

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'catalog.change_author'
	model = Author
	form_class = AuthorForm
	template_name_suffix = '_update_form'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'catalog.delete_author'
	model = Author
	success_url = reverse_lazy('authors_list')

class BookList(ListView):
	model = Book

	def get_context_data(self, **kwargs):
		if self.request.user.has_perm('catalog.add_book'):
			kwargs['form'] = BookForm()
		return super(ListView, self).get_context_data(**kwargs)

class BookDetail(DetailView):
	model = Book

	def get_context_data(self, **kwargs):
		user = self.request.user
		if hasattr(user, 'reader'):
			kwargs['user_is_reader'] = True
			user_book_ids = list([book.id for book in user.reader.books.all()])
			if self.get_object().id in user_book_ids:
				kwargs['book_in_reader_list'] = True
		return super(DetailView, self).get_context_data(**kwargs)

class BookUpdate(PermissionRequiredMixin, UpdateView):
	permission_required = 'catalog.change_book'
	model = Book
	form_class = BookForm
	template_name_suffix = '_update_form'

class BookDelete(PermissionRequiredMixin, DeleteView):
	permission_required = 'catalog.delete_book'
	model = Book
	success_url = reverse_lazy('books_list')

def reader_create_with_list(request):
	context_data = {}
	context_data['readers'] = Reader.objects.all()
	if request.method == 'POST':
		f = UserCreationForm(request.POST)
		if f.is_valid():
			new_user = f.save()
			readers_group = Group.objects.get(name = 'readers')
			new_user.groups.add(readers_group)
			new_user.save()
			Reader.objects.create(user = new_user)
			return redirect('login')
	elif not request.user.is_authenticated:
		context_data['register_reader_form'] = UserCreationForm()
	return render(request, 'catalog/reader_list.html', context_data)

def reader_detail(request, id):
	reader = Reader.objects.get(id__exact = id)

	if request.method == 'POST':
		for item in dict(request.POST):
			if 'book_id_' in item:
				prefix_length = len('book_id')
				book = Book.objects.get(id__exact = item[prefix_length + 1:])
				reader.books.add(book)

	return render(request, 'catalog/reader_detail.html', 
		{'reader': reader, 'other_books': reader.get_other_books()})

def book_delete_from_reader_list(request, reader_id, book_id):
	reader = Reader.objects.get(id = reader_id)
	book_to_delete = Book.objects.get(id__exact = book_id)
	reader.books.remove(book_to_delete)
	return redirect(reader.get_absolute_url())

def book_add_to_reader_list(request, reader_id, book_id):
	reader = Reader.objects.get(id = reader_id)
	book_to_add = Book.objects.get(id__exact = book_id)
	reader.books.add(book_to_add)
	return redirect(reader.get_absolute_url())
