from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
	first_name = models.CharField(max_length = 100, verbose_name = 'Имя', help_text = 'Введите имя автора')
	last_name = models.CharField(max_length = 100, verbose_name = 'Фамилия', help_text = 'Введите фамилию автора')
	date_of_birth = models.DateField(verbose_name = 'Дата рождения', help_text = 'Введите дату рождения автора в формате ГГГГ-ММ-ДД')
	date_of_death = models.DateField(null = True, blank = True, verbose_name = 'Дата смерти', help_text = 'Введите дату смерти автора в формате ГГГГ-ММ-ДД; поле необязательно')
	biography = models.TextField(verbose_name = 'Краткая биография', help_text = 'Введите краткую биографию автора')

	class Meta:
		ordering = ['last_name', 'first_name']

	def get_absolute_url(self):
		return reverse('author_detail', args = [str(self.id)])

	def __str__(self):
		return f'{self.first_name} {self.last_name}'

class Book(models.Model):
	title = models.CharField(max_length = 100, verbose_name = 'Название', help_text = 'Введите название книги')
	year = models.IntegerField(verbose_name = 'Год написания', help_text = 'Введите год написания книги')
	author = models.ForeignKey(Author, on_delete = models.SET_NULL, 
		null = True, blank = True, verbose_name = 'Автор', help_text = 'Выберите автора из списка')
	description = models.TextField(verbose_name = 'Краткое описание', help_text = 'Введите краткое описание книги')

	class Meta:
		ordering: ['title']

	def get_absolute_url(self):
		return reverse('book_detail', args = [str(self.id)])

	def __str__(self):
		return f'{ self.title } ({self.author}, {self.year})'

class Reader(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	books = models.ManyToManyField(Book)

	def get_books(self):
		return "; ".join([b.title for b in self.books.all()])

	def __str__(self):
		return f'{ self.user.username }'

	def get_absolute_url(self):
		return reverse('reader_detail', args = [str(self.id)])

	def get_other_books(self):
		reader_books = self.books.all()
		reader_book_ids = list([book.id for book in reader_books])
		other_books = Book.objects.all().exclude(id__in = reader_book_ids)
		return list(other_books)