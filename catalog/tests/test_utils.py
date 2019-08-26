from ..utils import get_unique_name
from django.test import TestCase

class GetUniqueNameTest(TestCase):
	
	def test_1(self):
		name_set = ['name_1', 'name_2', 'name_3', 'name_4']
		unique_name = get_unique_name(name_set)
		print(unique_name)
		self.assertFalse(unique_name in name_set)

	def test_2(self):
		name_set = ['new_user', 'name_1', 'name_2', 'name_3', 'name_4']
		unique_name = get_unique_name(name_set)
		print(unique_name)
		self.assertFalse(unique_name in name_set)

	def test_3(self):
		name_set = ['new_user', 'new_user_0', 'new_user_1', 'name_1', 'name_2', 'name_3', 'name_4']
		unique_name = get_unique_name(name_set)
		print(unique_name)
		self.assertFalse(unique_name in name_set)
