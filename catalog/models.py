from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	date_of_birth = models.DateField()
	date_of_death = models.DateField()
	biography = models.TextField()

	class Meta:
		ordering = ['last_name', 'first_name']

	def get_absolute_url(self):
		return reverse('author_detail', args = [str(self.id)])

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

class Book(models.Model):
	title = models.CharField(max_length = 100)
	year = models.IntegerField()
	author = models.ForeignKey(Author, on_delete = models.SET_NULL, 
		null = True, blank = True)
	description = models.TextField()

	class Meta:
		ordering: ['title']

	def get_absolute_url(self):
		return reverse('book_detail', args = [str(self.id)])

	def __str__(self):
		return f'{ self.title }'

class Reader(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	books = models.ManyToManyField(Book)

	def get_books(self):
		return "; ".join([b.title for b in self.books.all()])

	def __str__(self):
		return f'{ self.user.username }'