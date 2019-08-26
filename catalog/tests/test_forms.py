from django.test import TestCase
from ..forms import AuthorForm, BookForm
from datetime import timedelta, date

class AuthorFormTest(TestCase):
	def test_author_form_date_of_birth_is_earlier_than_today(self):
		future_date = date.today() + timedelta(days = 5)
		form = AuthorForm(data = {
			'date_of_birth': future_date,
			'first_name': 'bob',
			'last_name': 'bobson',
			'biography': 'it is biography',
			})
		self.assertFalse(form.is_valid())

	def test_author_form_date_of_death_is_earlier_than_today(self):
		future_date = date.today() + timedelta(days = 5)
		form = AuthorForm(data = {
			'date_of_birth': '1800-10-10',
			'date_of_death': future_date,
			'first_name': 'bob',
			'last_name': 'bobson',
			'biography': 'it is biography',
			})
		self.assertFalse(form.is_valid())

	def test_author_form_date_of_birth_is_earlier_than_date_of_death(self):
		date_of_death = date.today() - timedelta(days = 100000)
		date_of_birth = date_of_death + timedelta(days = 50000)

		form = AuthorForm(data = {
			'date_of_birth': date_of_birth,
			'date_of_death': date_of_death,
			'first_name': 'bob',
			'last_name': 'bobson',
			'biography': 'it is biography',
			})
		self.assertFalse(form.is_valid())

class BookFormTest(TestCase):
	def test_book_form_year_is_earlier_then_current(self):
		form = BookForm(data = {
			'title': 'title 1',
			'author': 1,
			'year': 2050,
			'description': 'it is description',
			})
		self.assertFalse(form.is_valid())