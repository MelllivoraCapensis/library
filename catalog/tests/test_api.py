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

	def setUp(self):
		pass

	def test_staff_get_author_list_json(self):
		client = StaffApiTest.staff_client
		response = client.get('/api/authors/')
		