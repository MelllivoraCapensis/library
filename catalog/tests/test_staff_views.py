from django.test import TestCase, Client
from ..models import Reader, Author, Book
from django.contrib.auth.forms import UserCreationForm
from ..utils import get_unique_name
from django.contrib.auth.models import User, Group
from ..forms import AuthorForm, BookForm
from re import findall

class StaffViewTest(TestCase):
	fixtures = ['all_data.json']

	@classmethod
	def setUpTestData(cls):
		username_set = [user.username for user in User.objects.all()]
		new_staff_name = get_unique_name(username_set)
		cls.credentials = {'username': new_staff_name, 'password': 'dima1234'}
		new_staff = User.objects.create_user(**cls.credentials)
		new_staff.groups.add(Group.objects.get(name = 'staff'))
		cls.staff_client = Client()
		cls.staff_client.login(**cls.credentials)

	def setUp(self):
		pass

	def test_staff_get_reader_list(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/readers/')
		derived_readers = list(response.context['readers'].order_by('id'))
		expected_readers = list(Reader.objects.all().order_by('id'))
		self.assertListEqual(expected_readers, derived_readers)

	def test_staff_don_t_get_register_form(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/readers/')
		self.assertFalse(hasattr(response.context, 'register_reader_form'))

	def test_staff_get_author_list(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/authors/')
		expected_authors = list(Author.objects.order_by('id'))
		derived_authors = list(response.context['author_list'].order_by('id'))
		self.assertListEqual(expected_authors, derived_authors)

	def test_staff_get_author_create_form(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/authors/')
		derived_form_class = response.context['form'].__class__
		self.assertEqual(derived_form_class, AuthorForm().__class__)

	def test_staff_get_update_author_link_in_author_list(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/authors/')
		content = str(response.content)
		update_link_href_pattern = r'/catalog/author/\d+/update/'
		matches = findall(update_link_href_pattern, content)
		update_link_num = len(matches)
		author_num = Author.objects.count()
		self.assertEqual(author_num, update_link_num)

	def test_staff_get_delete_author_link_in_author_list(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/authors/')
		content = str(response.content)
		delete_link_href_pattern = r'/catalog/author/\d+/delete/'
		matches = findall(delete_link_href_pattern, content)
		delete_link_num = len(matches)
		author_num = Author.objects.count()
		self.assertEqual(author_num, delete_link_num)

	

	def test_staff_get_book_list(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/books/')
		expected_books = list(Book.objects.order_by('id'))
		derived_books = list(response.context['book_list'].order_by('id'))
		self.assertListEqual(expected_books, derived_books)

	def test_staff_get_book_create_form(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/books/')
		derived_form_class = response.context['form'].__class__
		self.assertEqual(derived_form_class, BookForm().__class__)


	def test_staff_get_update_book_link_in_book_list(self):
			client = StaffViewTest.staff_client
			response = client.get('/catalog/books/')
			content = str(response.content)
			update_link_href_pattern = r'/catalog/book/\d+/update/'
			matches = findall(update_link_href_pattern, content)
			update_link_num = len(matches)
			book_num = Book.objects.count()
			self.assertEqual(book_num, update_link_num)

	def test_staff_get_delete_book_link_in_book_list(self):
		client = StaffViewTest.staff_client
		response = client.get('/catalog/books/')
		content = str(response.content)
		delete_link_href_pattern = r'/catalog/book/\d+/delete/'
		matches = findall(delete_link_href_pattern, content)
		delete_link_num = len(matches)
		book_num = Book.objects.count()
		self.assertEqual(book_num, delete_link_num)

