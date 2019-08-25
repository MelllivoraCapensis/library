from django.test import TestCase
from ..forms import AuthorForm
from datetime import timedelta, date

class AuthorFormTest(TestCase):
	def test_update_author_form_date_of_birth_is_earlier_than_today(self):
		future_date = date.today() + timedelta(days = 5)
		form = AuthorUpdateForm(data = {
			'date_of_birth': future_date,
			'first_name': 'bob',
			'last_name': 'bobson',
			'biography': 'it is biography',
			})
		self.assertFalse(form.is_valid())

	def test_update_author_form_date_of_death_is_earlier_than_today(self):
		future_date = date.today() + timedelta(days = 5)
		form = AuthorUpdateForm(data = {
			'date_of_birth': '1800-10-10',
			'date_of_death': future_date,
			'first_name': 'bob',
			'last_name': 'bobson',
			'biography': 'it is biography',
			})
		self.assertFalse(form.is_valid())

	def test_update_author_form_date_of_birth_is_earlier_than_date_of_death(self):
		date_of_death = date.today() - timedelta(days = 100000)
		date_of_birth = date_of_death + timedelta(days = 50000)

		form = AuthorUpdateForm(data = {
			'date_of_birth': date_of_birth,
			'date_of_death': date_of_death,
			'first_name': 'bob',
			'last_name': 'bobson',
			'biography': 'it is biography',
			})
		self.assertFalse(form.is_valid())