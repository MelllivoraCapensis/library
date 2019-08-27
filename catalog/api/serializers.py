from rest_framework import serializers
from ..models import Author, Book, Reader
from datetime import date

class AuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Author
		fields = '__all__'

	def validate(self, data):
		if data['date_of_birth'] > date.today():
			raise serializers.ValidationError('Вы не можете предсказать дату рождения автора')
		if 'date_of_death' in data.keys():
			if data['date_of_death'] < data['date_of_birth']:
				raise serializers.ValidationError('Дата смерти не может быть раньше даты рождения')
			if data['date_of_death'] > date.today():
				raise serializers.ValidationError('Вы не можете предсказать дату смерти автора')
		return data

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = '__all__'

	def validate(self, data):
		if data['year'] > date.today().year:
			raise serializers.ValidationError('Книга не может выйти в будущем')
		return data

class ReaderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reader
		fields = '__all__'