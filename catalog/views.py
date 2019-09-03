from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Author, Book, Reader, Grade
from django import forms
from .forms import AuthorForm, BookForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

class AuthorList(ListView):
	model = Author
	paginate_by = 5

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
	paginate_by = 5

	def get_context_data(self, **kwargs):
		if self.request.user.has_perm('catalog.add_book'):
			kwargs['form'] = BookForm()
		return super(ListView, self).get_context_data(**kwargs)

class BookDetail(DetailView):
	model = Book

	def get_context_data(self, **kwargs):
		user = self.request.user
		if hasattr(user, 'reader'):
			grade = Grade.objects.filter(
				reader__id = user.reader.id).filter(
				book__id = self.object.id)
			if grade:
				kwargs['grade'] = grade[0]
			
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
	context = {}
	context['readers'] = Reader.objects.all()
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
		context['register_reader_form'] = UserCreationForm()
	return render(request, 'catalog/reader_list.html', context)

def reader_detail(request, id):
	reader = get_object_or_404(Reader, id = id)
	context = {}
	if request.method == 'POST':
		for item in dict(request.POST):
			if 'book_id_' in item:
				prefix_length = len('book_id')
				book = Book.objects.get(id__exact = item[prefix_length + 1:])
				reader.books.add(book)

	if request.user.is_authenticated:
		if request.user.id == reader.user.id:
			context['other_books'] = reader.get_other_books()
	
	context['reader'] = reader 
	return render(request, 'catalog/reader_detail.html', 
		context = context)

class ReaderUpdate(UpdateView):
	model = Reader
	fields = ('image',)
	template_name_suffix = '_update_form'

	def can_change_avatar(func):
		def func_wrapper(self, request, *args, **kwargs):
			if not hasattr(request.user, 'reader'):
				return HttpResponseForbidden()
			self.object = self.get_object()
			if self.object.id != request.user.reader.id:
				return HttpResponseForbidden()
			return func(self, request, *args, **kwargs)

		return func_wrapper

	@can_change_avatar	
	def get(self, request, *args, **kwargs):		
		return super(UpdateView, self).get(request, *args, **kwargs)

	@can_change_avatar
	def post(self, request, *args, **kwargs):
		return super(UpdateView, self).post(request, *args, **kwargs)


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

