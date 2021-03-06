from django.forms import ModelForm, ValidationError
from .models import Author, Book
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

class BookForm(ModelForm):
	VALID_EXTENSIONS = ('pdf', 'doc', 'djvu', 'docx', 'rtf', 'txt')
	class Meta:
		model = Book
		fields = '__all__'

	def clean_year(self):
		if date.today().year < self.cleaned_data['year']:
			raise ValidationError('Дата выпуска книги не может быть позже текущего года')
		return self.cleaned_data['year']

	def clean_file(self):
		file_name = self.cleaned_data['file'].name
		point_index = int(file_name.rfind('.'))

		if point_index == -1:
			raise ValidationError('Недопустимое имя файла')
			
		file_ext = file_name[point_index + 1:]

		if file_ext not in self.VALID_EXTENSIONS:
			raise ValidationError('Недопустимое расширение файла')

		return self.cleaned_data['file']

