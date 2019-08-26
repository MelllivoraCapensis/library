from django.test import TestCase
from ..models import Author, Reader, Book
from django.contrib.auth.models import User, Group

class AuthorModelTest(TestCase):
	fixtures = ['authors.json']

	@classmethod
	def setUpTestData(cls):
		cls.author = Author.objects.create(first_name = 'Big', 
			last_name = 'Bob', date_of_birth = '1900-10-11',
			date_of_death = '2000-02-01', biography = 'it is biography')

	def setUp(self):
		pass

	def test_first_name_label(self):
		field_label = AuthorModelTest.author._meta.get_field('first_name').verbose_name
		self.assertEquals(field_label, 'Имя')

	def test_last_name_label(self):
		field_label = AuthorModelTest.author._meta.get_field('last_name').verbose_name
		self.assertEquals(field_label, 'Фамилия')

	def test_date_of_birth_label(self):
		field_label = AuthorModelTest.author._meta.get_field('date_of_birth').verbose_name
		self.assertEquals(field_label, 'Дата рождения')

	def test_date_of_death_label(self):
		field_label = AuthorModelTest.author._meta.get_field('date_of_death').verbose_name
		self.assertEquals(field_label, 'Дата смерти')

	def test_biography_label(self):
		field_label = AuthorModelTest.author._meta.get_field('biography').verbose_name
		self.assertEquals(field_label, 'Краткая биография')

	def test_author_str_is_first_name_space_last_name(self):
		for author in Author.objects.all():
			expected_name = f'{author.first_name} {author.last_name}'
			self.assertEquals(expected_name, str(author))

	def test_author_get_absolute_url(self):
		for author in Author.objects.all():
			self.assertEquals(author.get_absolute_url(),
			f'/catalog/author/{author.id}/')

class ReaderModelTest(TestCase):
	fixtures = ['authors.json', 'user_groups.json', 'users.json']
	
	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create(username = 'Bob', password = 'dima1234')
		cls.user.groups.add(Group.objects.get(name = 'readers'))
		cls.reader = Reader.objects.create(user = cls.user)
		cls.other_books = []

		for i in range(1, 10):
			book = Book.objects.create(title = f'title {i}', 
				author = Author.objects.get(id = 1), 
				year = 2000 + i, description = f'description{i}')
			if i % 2 == 1:
				cls.reader.books.add(book)
			else:
				cls.other_books.append(book)

	def setUp(self):
		pass

	def test_reader_get_other_books(self):
		self.assertEquals(ReaderModelTest.reader.get_other_books(), 
			ReaderModelTest.other_books)	

	def test_reader_get_absolute_url(self):
		for reader in Reader.objects.all():
			self.assertEquals(reader.get_absolute_url(), 
				f'/catalog/reader/{reader.id}/')

	def test_reader_get_books(self):
		self.assertEquals(ReaderModelTest.reader.get_books(),
			'title 1; title 3; title 5; title 7; title 9')

class BookModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.author = Author.objects.create(first_name = 'Bob',
			last_name = 'Bobson', date_of_birth = '1900-10-10',
			date_of_death = '1995-1-5')
		cls.book = Book.objects.create(title = 'The Good Book',
			year = 1950, description = 'it is description', author = cls.author)

	def setUp(self):
		pass

	def test_str_book(self):
		self.assertEquals(str(BookModelTest.book), 
			'The Good Book (Bob Bobson, 1950)')

	def test_book_get_absolute_url(self):
		book_id = BookModelTest.book.id
		self.assertEquals(BookModelTest.book.get_absolute_url(),
			f'/catalog/book/{book_id}/')

	def test_title_label(self):
		self.assertEquals(BookModelTest.book._meta.get_field('title').verbose_name,
			'Название')

	def test_year_label(self):
		self.assertEquals(BookModelTest.book._meta.get_field('year').verbose_name,
			'Год написания')

	def test_author_label(self):
		self.assertEquals(BookModelTest.book._meta.get_field('author').verbose_name,
			'Автор')

	def test_description_label(self):
		self.assertEquals(BookModelTest.book._meta.get_field('description').verbose_name,
			'Краткое описание')


