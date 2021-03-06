from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from library import settings
import os
from django.core.files.images import ImageFile
from sorl.thumbnail import get_thumbnail
from django.contrib.sites.models import Site
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Author(models.Model):
	
	first_name = models.CharField(max_length = 100, verbose_name = 'Имя', help_text = 'Введите имя автора')
	last_name = models.CharField(max_length = 100, verbose_name = 'Фамилия', help_text = 'Введите фамилию автора')
	date_of_birth = models.DateField(verbose_name = 'Дата рождения', help_text = 'Введите дату рождения автора в формате ГГГГ-ММ-ДД')
	date_of_death = models.DateField(null = True, blank = True, verbose_name = 'Дата смерти', help_text = 'Введите дату смерти автора в формате ГГГГ-ММ-ДД; поле необязательно')
	biography = models.TextField(verbose_name = 'Краткая биография', help_text = 'Введите краткую биографию автора')
	image = models.ImageField(upload_to = 'authors', verbose_name = 'Изображение автора', 
		null = True, blank = True, default = None, help_text = 'Выберите изображение автора')

	IMAGE_WIDTH_LARGE = 200
	IMAGE_HEIGHT_SMALL = 60



	class Meta:
		ordering = ['last_name', 'first_name']

	def get_absolute_url(self):
		return reverse('author_detail', args = [str(self.id)])

	def get_image_small(self):
		if self.image:
			return get_thumbnail(self.image, 'x' + str(
				self.IMAGE_HEIGHT_SMALL))
		return get_thumbnail(os.path.join(os.getcwd(), 
			'media/author_default.png'),
		 'x' + str(self.IMAGE_HEIGHT_SMALL))

	def get_image_large(self):
		if self.image:
			return get_thumbnail(self.image, str(self.IMAGE_WIDTH_LARGE))
		return get_thumbnail(os.path.join(os.getcwd(), 
			'media/author_default.png'),
				str(self.IMAGE_WIDTH_LARGE))


	def get_average_grade(self):
		books_with_grade = [b for b in self.book_set.all() if b.get_average_grade()]
		if not books_with_grade:
			return False
		s = 0
		n = 0
		for book in books_with_grade:
			grades = list([g.value for g in book.grade_set.all()])
			s += sum(grades)
			n += len(grades)
		return round(s / n, 2)

	def get_grades_count(self):
		books_with_grade = [b for b in self.book_set.all() if b.get_average_grade()]
		if not books_with_grade:
			return False
		n = 0
		for book in books_with_grade:
			n += book.grade_set.count()
		return n




	def __str__(self):
		return f'{self.first_name} {self.last_name}'

class Book(models.Model):
	title = models.CharField(max_length = 100, 
		verbose_name = 'Название', help_text = 'Введите название книги')
	year = models.IntegerField(verbose_name = 'Год написания', 
		help_text = 'Введите год написания книги')
	author = models.ForeignKey(Author, on_delete = models.SET_NULL, 
		null = True, blank = True, verbose_name = 'Автор', 
		help_text = 'Выберите автора из списка')
	description = models.TextField(verbose_name = 'Краткое описание', 
		help_text = 'Введите краткое описание книги')
	file = models.FileField(upload_to = 'books', null = True,
		blank = True, default = None, verbose_name = 'Файл', 
		help_text = 'Добавьте файл')
	image = models.ImageField(upload_to = 'books', 
		null = True, blank = True, default = None, 
		verbose_name = 'Изображение книги', help_text = 'Добавьте изображение книги')
	

	IMAGE_WIDTH_LARGE = 300
	IMAGE_HEIGHT_SMALL = 60


	class Meta:
		ordering: ['title']

	def get_absolute_url(self):
		return reverse('book_detail', args = [str(self.id)])

	def get_image_small(self):
		if self.image:
			return get_thumbnail(self.image, 'x' + str(
				self.IMAGE_HEIGHT_SMALL))
		return get_thumbnail(os.path.join(os.getcwd(), 
			'media/book_default.png'),
			 'x' + str(self.IMAGE_HEIGHT_SMALL))

	def get_image_large(self):
		if self.image:
			return get_thumbnail(self.image, 
				str(self.IMAGE_WIDTH_LARGE))
		return get_thumbnail(os.path.join(os.getcwd(), 
			'media/book_default.png'), str(self.IMAGE_WIDTH_LARGE))

	def get_average_grade(self):
		grades = [g.value for g in self.grade_set.all()]
		if not grades:
			return False
		return round(sum(grades) / len(grades), 2)

	def get_grades_count(self):
		if self.get_average_grade():
			return len(self.grade_set.all())

	def __str__(self):
		return f'{ self.title } ({self.author}, {self.year})'



class Reader(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	books = models.ManyToManyField(Book)
	image = models.ImageField(upload_to = 'users', null = True,
		blank = True, verbose_name = 'Изображение', help_text = 'Выберите изображение png/jpg')

	IMAGE_WIDTH_LARGE = 200
	IMAGE_HEIGHT_SMALL = 60

	def get_books(self):
		return "; ".join([b.title for b in self.books.all()])

	def __str__(self):
		return f"{ self.user.username }"

	def get_book_list_url(self):
		return reverse_lazy('reader_book_list', args = [str(self.id)])

	def get_grade_list_url(self):
		return reverse_lazy('reader_grade_list', args = [str(self.id)])

	def get_absolute_url(self):
		return self.get_book_list_url()

	def get_other_books(self, num_books):
		reader_books = self.books.all()
		reader_book_ids = list([book.id for book in reader_books])
		other_books = list(Book.objects.exclude(id__in = reader_book_ids))
		other_books.sort(key = lambda obj: - obj.get_average_grade())
		return other_books[:num_books]

	def get_image_small(self):
		if self.image:
			return get_thumbnail(self.image, 'x' + str(
				self.IMAGE_HEIGHT_SMALL))
		return get_thumbnail(os.path.join(os.getcwd(),
		 'media/user_default.png'), 'x' + str(self.IMAGE_HEIGHT_SMALL))

class Grade(models.Model):
	reader = models.ForeignKey(Reader, on_delete = models.CASCADE)
	book = models.ForeignKey(Book, on_delete = models.CASCADE)
	value = models.IntegerField(null = True, blank = True, 
		verbose_name = 'Оценить книгу', help_text = 'Оцените книгу от 1 до 10', 
		validators = [MaxValueValidator(10), MinValueValidator(1)])

	


