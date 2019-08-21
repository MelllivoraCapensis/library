from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Author, Book, Reader

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
