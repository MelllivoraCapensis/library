from django.forms import ModelForm, ValidationError
from .models import Author
from datetime import date
	

class AuthorForm(ModelForm):
	class Meta:
		model = Author
		fields = '__all__'

	def clean_date_of_death(self):
		if self.cleaned_data['date_of_death'] != None:
			if self.cleaned_data['date_of_death'] < self.cleaned_data['date_of_birth']:
				raise ValidationError('Дата смерти не может быть раньше даты рождения')
			if self.cleaned_data['date_of_death'] > date.today():
				raise ValidationError('Вы не можете предсказать дату смерти автора')
			return self.cleaned_data['date_of_death']

	def clean_date_of_birth(self):
		if self.cleaned_data['date_of_birth'] != None:
			if self.cleaned_data['date_of_birth'] > date.today():
				raise ValidationError('Вы не можете предсказать дату рождения автора')
			return self.cleaned_data['date_of_birth']

	# def clean_date_of_death(self):
	# 	return self.cleaned_data['date_of_death'] > self.clean_data['date_of_birth']



