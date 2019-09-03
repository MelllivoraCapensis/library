from rest_framework.test import APIClient
from ..utils import get_unique_name
from django.test import TestCase
from ..models import Author, Book, Reader
from django.contrib.auth.models import Group, User

class StaffApiTest(TestCase):
	fixtures = ['all_data.json']

	@classmethod
	def setUpTestData(cls):
		username_set = [user.username for user in User.objects.all()]
		new_staff_name = get_unique_name(username_set)
		cls.credentials = {'username': new_staff_name, 'password': 'dima1234'}
		new_staff = User.objects.create_user(**cls.credentials)
		new_staff.groups.add(Group.objects.get(name = 'staff'))
		cls.staff_client = APIClient()
		cls.staff_client.login(**cls.credentials)

		test_author = Author.objects.create(first_name = 'Test Author', last_name = 'Test Author',
			date_of_birth = '1200-02-25', date_of_death = '1300-12-10',
			biography = 'it is test author for updating and deleting tests')
		test_book = Book.objects.create(title = 'Test Book', author = test_author, year = 1500,
			description = 'it is test book for updating and deleting tests')


	def setUp(self):
		pass

	def test_staff_get_author_list(self):
		client = StaffApiTest.staff_client
		response = client.get('/api/authors/')
		derived_author_ids = [a['id'] for a in response.json()]
		derived_author_ids.sort()
		expected_author_ids = list([a.id for a in Author.objects.order_by('id')])
		self.assertListEqual(expected_author_ids, derived_author_ids)

	def test_staff_can_add_author_via_api(self):
		client = StaffApiTest.staff_client
		author_data = {
			'first_name': 'Billy',
			'last_name': 'Jean',
			'date_of_birth': '1950-10-18',
			'biography': 'nothing is known',
		}
		response = client.post('/api/authors/', data = author_data, format = 'multipart')
		self.assertTrue(response.status_code == 201 and Author.objects.get(first_name = 'Billy'))

	def test_staff_get_book_list(self):
		client = StaffApiTest.staff_client
		response = client.get('/api/books/')
		derived_book_ids = [b['id'] for b in response.json()]
		derived_book_ids.sort()
		expected_book_ids = list([a.id for a in Book.objects.order_by('id')])
		self.assertListEqual(expected_book_ids, derived_book_ids)

	def test_staff_can_add_book_via_api(self):
		client = StaffApiTest.staff_client
		book_data = {
			'title': 'The book',
			'author': 1,
			'year': 2000,
			'description': 'nothing is known',
		}
		response = client.post('/api/books/', data = book_data,
			format = 'multipart')
		self.assertTrue(response.status_code == 201 and Book.objects.get(title = 'The book'))

	def test_staff_can_update_book_via_api(self):
		client = StaffApiTest.staff_client
		test_book = Book.objects.get(title = 'Test Book')
		response = client.put(f'/api/book/{test_book.id}/', data = {
			'title': 'Test Book After Updating',
			'year': test_book.year,
			'author': test_book.author.id,
			'description': test_book.description
			}, format = 'multipart')
		self.assertTrue(response.status_code == 200)
		self.assertEqual(Book.objects.get(id = test_book.id).title, 'Test Book After Updating')

	def test_staff_can_delete_book_via_api(self):
		client = StaffApiTest.staff_client
		test_book = Book.objects.get(title = 'Test Book')
		response = client.delete(f'/api/book/{test_book.id}/')
		self.assertTrue(response.status_code == 204)
		self.assertFalse(Book.objects.filter(id = test_book.id))

	def test_staff_can_update_author_via_api(self):
		client = StaffApiTest.staff_client
		test_author = Author.objects.get(first_name = 'Test Author')
		response = client.put(f'/api/author/{test_author.id}/', data = {
			'first_name': test_author.first_name,
			'last_name': 'Test Author After Updating',
			'date_of_birth': test_author.date_of_birth,
			'biography': test_author.biography,
			}, format = 'multipart')
		self.assertTrue(response.status_code == 200)
		self.assertEqual(Author.objects.get(id = test_author.id).last_name, 
			'Test Author After Updating')

	def test_staff_can_delete_author_via_api(self):
		client = StaffApiTest.staff_client
		test_author = Author.objects.get(first_name = 'Test Author')
		response = client.delete(f'/api/author/{test_author.id}/')
		self.assertTrue(response.status_code == 204)
		self.assertFalse(Author.objects.filter(id = test_author.id))



class ReaderApiTest(TestCase):
	fixtures = ['all_data.json']

	@classmethod
	def setUpTestData(cls):
		username_set = [user.username for user in User.objects.all()]
		new_reader_name = get_unique_name(username_set)
		cls.credentials = {'username': new_reader_name, 'password': 'dima1234'}
		new_reader = User.objects.create_user(**cls.credentials)
		new_reader.groups.add(Group.objects.get(name = 'readers'))
		cls.reader_client = APIClient()
		cls.reader_client.login(**cls.credentials)

		test_author = Author.objects.create(first_name = 'Test Author', last_name = 'Test Author',
			date_of_birth = '1200-02-25', date_of_death = '1300-12-10',
			biography = 'it is test author for updating and deleting tests')
		test_book = Book.objects.create(title = 'Test Book', author = test_author, year = 1500,
			description = 'it is test book for updating and deleting tests')

	def setUp(self):
		pass

	def test_reader_get_author_list(self):
		client = ReaderApiTest.reader_client
		response = client.get('/api/authors/')
		derived_author_ids = [a['id'] for a in response.json()]
		derived_author_ids.sort()
		expected_author_ids = list([a.id for a in Author.objects.order_by('id')])
		self.assertListEqual(expected_author_ids, derived_author_ids)

	def test_reader_cannot_add_author_via_api(self):
		client = ReaderApiTest.reader_client
		author_data = {
			'first_name': 'Billy',
			'last_name': 'Jean',
			'date_of_birth': '1950-10-18',
			'biography': 'nothing is known',
		}
		response = client.post('/api/authors/', data = author_data, format = 'multipart')
		self.assertTrue(response.status_code == 403)

	def test_reader_get_book_list(self):
		client = ReaderApiTest.reader_client
		response = client.get('/api/books/')
		derived_book_ids = [a['id'] for a in response.json()]
		derived_book_ids.sort()
		expected_book_ids = list([a.id for a in Book.objects.order_by('id')])
		self.assertListEqual(expected_book_ids, derived_book_ids)

	def test_reader_cannot_add_book_via_api(self):
		client = ReaderApiTest.reader_client
		book_data = {
			'title': 'The book',
			'author': 1,
			'year': 2000,
			'description': 'nothing is known',
		}
		response = client.post('/api/authors/', data = book_data, format = 'multipart')
		self.assertTrue(response.status_code == 403)


	def test_reader_cannot_update_book_via_api(self):
		client = ReaderApiTest.reader_client
		test_book = Book.objects.get(title = 'Test Book')
		response = client.put(f'/api/book/{test_book.id}/', data = {
			'title': 'Test Book After Updating',
			'year': test_book.year,
			'author': test_book.author.id,
			'description': test_book.description
			}, format = 'multipart')
		self.assertTrue(response.status_code == 403)

	def test_reader_cannot_delete_book_via_api(self):
		client = ReaderApiTest.reader_client
		test_book = Book.objects.get(title = 'Test Book')
		response = client.delete(f'/api/book/{test_book.id}/')
		self.assertTrue(response.status_code == 403)
		self.assertTrue(Book.objects.filter(id = test_book.id))

	def test_reader_cannot_update_author_via_api(self):
		client = ReaderApiTest.reader_client
		test_author = Author.objects.get(first_name = 'Test Author')
		response = client.put(f'/api/author/{test_author.id}/', data = {
			'first_name': test_author.first_name,
			'last_name': 'Test Author After Updating',
			'date_of_birth': test_author.date_of_birth,
			'biography': test_author.biography,
			}, format = 'multipart')
		self.assertTrue(response.status_code == 403)

	def test_reader_cannot_delete_author_via_api(self):
		client = ReaderApiTest.reader_client
		test_author = Author.objects.get(first_name = 'Test Author')
		response = client.delete(f'/api/author/{test_author.id}/')
		self.assertTrue(response.status_code == 403)
		self.assertTrue(Author.objects.filter(id = test_author.id))



class AnonApiTest(TestCase):
	fixtures = ['all_data.json']

	@classmethod
	def setUpTestData(cls):
		cls.anon_client = APIClient()

		test_author = Author.objects.create(first_name = 'Test Author', last_name = 'Test Author',
			date_of_birth = '1200-02-25', date_of_death = '1300-12-10',
			biography = 'it is test author for updating and deleting tests')
		test_book = Book.objects.create(title = 'Test Book', author = test_author, year = 1500,
			description = 'it is test book for updating and deleting tests')

	def setUp(self):
		pass

	def test_anon_get_author_list(self):
		client = AnonApiTest.anon_client
		response = client.get('/api/authors/')
		derived_author_ids = [a['id'] for a in response.json()]
		derived_author_ids.sort()
		expected_author_ids = list([a.id for a in Author.objects.order_by('id')])
		self.assertListEqual(expected_author_ids, derived_author_ids)

	def test_anon_cannot_add_author_via_api(self):
		client = AnonApiTest.anon_client
		author_data = {
			'first_name': 'Billy',
			'last_name': 'Jean',
			'date_of_birth': '1950-10-18',
			'biography': 'nothing is known',
		}
		response = client.post('/api/authors/', data = author_data, format = 'multipart')
		self.assertTrue(response.status_code == 403)

	def test_anon_get_book_list(self):
		client = AnonApiTest.anon_client
		response = client.get('/api/books/')
		derived_book_ids = [a['id'] for a in response.json()]
		derived_book_ids.sort()
		expected_book_ids = list([a.id for a in Book.objects.order_by('id')])
		self.assertListEqual(expected_book_ids, derived_book_ids)

	def test_anon_cannot_add_book_via_api(self):
		client = AnonApiTest.anon_client
		book_data = {
			'title': 'The book',
			'author': 1,
			'year': 2000,
			'description': 'nothing is known',
		}
		response = client.post('/api/books/', data = book_data, format = 'multipart')
		self.assertTrue(response.status_code == 403)

	def test_anon_cannot_update_book_via_api(self):
		client = AnonApiTest.anon_client
		test_book = Book.objects.get(title = 'Test Book')
		response = client.put(f'/api/book/{test_book.id}/', data = {
			'title': 'Test Book After Updating',
			'year': test_book.year,
			'author': test_book.author.id,
			'description': test_book.description
			}, format = 'multipart')
		self.assertTrue(response.status_code == 403)

	def test_anon_cannot_delete_book_via_api(self):
		client = AnonApiTest.anon_client
		test_book = Book.objects.get(title = 'Test Book')
		response = client.delete(f'/api/book/{test_book.id}/')
		self.assertTrue(response.status_code == 403)
		self.assertTrue(Book.objects.filter(id = test_book.id))

	def test_anon_cannot_update_author_via_api(self):
		client = AnonApiTest.anon_client
		test_author = Author.objects.get(first_name = 'Test Author')
		response = client.put(f'/api/author/{test_author.id}/', data = {
			'first_name': test_author.first_name,
			'last_name': 'Test Author After Updating',
			'date_of_birth': test_author.date_of_birth,
			'biography': test_author.biography,
			}, format = 'multipart')
		self.assertTrue(response.status_code == 403)

	def test_anon_cannot_delete_author_via_api(self):
		client = AnonApiTest.anon_client
		test_author = Author.objects.get(first_name = 'Test Author')
		response = client.delete(f'/api/author/{test_author.id}/')
		self.assertTrue(response.status_code == 403)
		self.assertTrue(Author.objects.filter(id = test_author.id))


		