from django.test import TestCase, Client
from ..models import Reader, Author, Book
from django.contrib.auth.forms import UserCreationForm
from ..utils import get_unique_name
from django.contrib.auth.models import User, Group
from re import findall


class ReaderViewTest(TestCase):
	fixtures = ['all_data.json']

	@classmethod
	def setUpTestData(cls):
		username_set = [user.username for user in User.objects.all()]
		new_reader_name = get_unique_name(username_set)
		new_reader = User.objects.create_user(username = new_reader_name, 
			password = 'dima1234')
		new_reader.groups.add(Group.objects.get(name = 'readers'))
		cls.reader_client = Client()
		cls.reader_client.login(username = new_reader.username,
			password = new_reader.password,)

	def test_reader_get_reader_list(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/readers/')
		derived_readers = list(response.context['readers'].order_by('id'))
		expected_readers = list(Reader.objects.all().order_by('id'))
		self.assertListEqual(expected_readers, derived_readers)

	def test_reader_don_t_get_register_form(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/readers/')
		self.assertFalse(hasattr(response.context, 'register_reader_form'))

	def test_reader_get_author_list(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/authors/')
		expected_authors = list(Author.objects.order_by('id'))
		derived_authors = list(response.context['author_list'].order_by('id'))
		self.assertListEqual(expected_authors, derived_authors)

	def test_reader_don_t_get_author_create_form(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/authors/')
		self.assertFalse(hasattr(response.context,
			'form'))

	def test_reader_cannot_create_author(self):
		client = ReaderViewTest.reader_client
		response = client.post('/catalog/authors/', data = {
			'first_name': 'Kevin',
			'last_name': 'Dude',
			'date_of_birth': '1900-11-12',
			'biography': 'he was not bad dude',
			})
		self.assertEqual(response.status_code, 405)

	def test_reader_don_t_get_update_author_link_in_author_list(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/authors/')
		content = str(response.content)
		update_link_href_pattern = r'/catalog/author/\d+/update/'
		matches = findall(update_link_href_pattern, content)
		self.assertFalse(matches)

	def test_reader_don_t_get_delete_author_link_in_author_list(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/authors/')
		content = str(response.content)
		delete_link_href_pattern = r'/catalog/author/\d+/delete/'
		matches = findall(delete_link_href_pattern, content)
		self.assertFalse(matches)


	def test_reader_get_book_list(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/books/')
		derived_books = list(
			response.context['book_list'].order_by('id'))
		expected_books = list(
			Book.objects.order_by('id'))
		self.assertListEqual(derived_books, expected_books)

	def test_reader_don_t_get_book_create_form(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/books/')
		self.assertFalse(hasattr(response.context,
			'form'))

	def test_reader_cannot_create_book(self):
		client = ReaderViewTest.reader_client
		response = client.post('/catalog/books/', data = {
			'title': 'The book',
			'year': 2005,
			'author': 1,
			'description': 'boring books',
			})
		self.assertEqual(response.status_code, 405)

	def test_reader_don_t_get_update_book_link_in_book_list(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/books/')
		content = str(response.content)
		update_link_href_pattern = r'/catalog/book/\d+/update/'
		matches = findall(update_link_href_pattern, content)
		self.assertFalse(matches)

	def test_reader_don_t_get_delete_book_link_in_book_list(self):
		client = ReaderViewTest.reader_client
		response = client.get('/catalog/books/')
		content = str(response.content)
		delete_link_href_pattern = r'/catalog/book/\d+/delete/'
		matches = findall(delete_link_href_pattern, content)
		self.assertFalse(matches)




