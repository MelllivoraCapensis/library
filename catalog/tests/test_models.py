from django.test import TestCase
from ..models import Author

class AuthorModelTest(TestCase):
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

	def test_author_name_is_last_name_comma_first_name(self):
		author = AuthorModelTest.author
		expected_name = f'{author.last_name}, {author.first_name}'
		self.assertEquals(expected_name, str(author))

	def test_author_absolute_url(self):
		self.assertEquals(AuthorModelTest.author.get_absolute_url(),
			'/catalog/author/1/')
