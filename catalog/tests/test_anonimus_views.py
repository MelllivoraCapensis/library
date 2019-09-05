from django.test import TestCase, Client
from ..models import Reader, Author, Book
from django.contrib.auth.forms import UserCreationForm
from ..utils import get_unique_name
from django.contrib.auth.models import User, Group
from re import findall
from ..views import BookList, AuthorList

class AnonimusViewTest(TestCase):
	fixtures = ['all_data.json']

	@classmethod
	def setUpTestData(cls):
		pass

	def setUp(self):
		pass

	def test_anon_get_reader_list(self):
		client = Client()
		response = client.get('/catalog/readers/')
		derived_readers = list(
			response.context['readers'])
		expected_readers = list(
			Reader.objects.all())[:5]

		self.assertListEqual(derived_readers, expected_readers,)

	def test_anon_get_register_form(self):
		client = Client()
		response = client.get('/catalog/readers/')
		derived_form_class = response.context['register_reader_form'].__class__
		expected_form_class = UserCreationForm

		self.assertEqual(expected_form_class, derived_form_class)

	def test_anon_can_register_as_user_and_reader(self):
		username_set = [user.username for user in User.objects.all()]
		new_username = get_unique_name(username_set)
		client = Client()
		response = client.post('/catalog/readers/', data = {
			'username': new_username,
			'password1': 'dima1234',
			'password2': 'dima1234',
			})
		new_user = User.objects.get(username = new_username)
		
		self.assertTrue(new_user and new_user.reader and 
			new_user in Group.objects.get(name = 'readers').user_set.all())

	def test_anon_get_author_list(self):
		client = Client()
		response = client.get('/catalog/authors/')
		derived_authors = list(
			response.context['author_list'])
		expected_authors = list(
			Author.objects.all())[:AuthorList.paginate_by]
		self.assertListEqual(derived_authors, expected_authors)

	def test_anon_don_t_get_author_create_form(self):
		client = Client()
		response = client.get('/catalog/authors/')
		self.assertFalse(hasattr(response.context,
			'form'))

	def test_anon_cannot_create_author(self):
		client = Client()
		response = client.post('/catalog/authors/', data = {
			'first_name': 'Kevin',
			'last_name': 'Dude',
			'date_of_birth': '1900-11-12',
			'biography': 'he was not bad dude',
			})
		self.assertEqual(response.status_code, 405)

	def test_anon_don_t_get_update_author_link_in_author_list(self):
		client = Client()
		response = client.get('/catalog/authors/')
		content = str(response.content)
		update_link_href_pattern = r'/catalog/author/\d+/update/'
		matches = findall(update_link_href_pattern, content)
		self.assertFalse(matches)

	def test_anon_don_t_get_delete_author_link_in_author_list(self):
		client = Client()
		response = client.get('/catalog/authors/')
		content = str(response.content)
		delete_link_href_pattern = r'/catalog/author/\d+/delete/'
		matches = findall(delete_link_href_pattern, content)
		self.assertFalse(matches)

	def test_anon_get_book_list(self):
		client = Client()
		response = client.get('/catalog/books/')
		derived_books = list(
			response.context['book_list'])
		expected_books = list(
			Book.objects.all())[:BookList.paginate_by]
		self.assertListEqual(derived_books, expected_books)

	def test_anon_don_t_get_book_create_form(self):
		client = Client()
		response = client.get('/catalog/books/')
		self.assertFalse(hasattr(response.context,
			'form'))

	def test_anon_cannot_create_book(self):
		client = Client()
		response = client.post('/catalog/books/', data = {
			'title': 'The book',
			'year': 2005,
			'author': 1,
			'description': 'boring books',
			})
		self.assertEqual(response.status_code, 405)

	def test_anon_don_t_get_update_book_link_in_book_list(self):
		client = Client()
		response = client.get('/catalog/books/')
		content = str(response.content)
		update_link_href_pattern = r'/catalog/book/\d+/update/'
		matches = findall(update_link_href_pattern, content)
		self.assertFalse(matches)

	def test_anon_don_t_get_delete_book_link_in_book_list(self):
		client = Client()
		response = client.get('/catalog/books/')
		content = str(response.content)
		delete_link_href_pattern = r'/catalog/book/\d+/delete/'
		matches = findall(delete_link_href_pattern, content)
		self.assertFalse(matches)

