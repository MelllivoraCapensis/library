from rest_framework import serializers
from ..models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Author
		fields = '__all__'

	def validate(self, data):
		if data['date_of_death'] < data['date_of_birth']:
			raise serializers.ValidationError('Дата смерти не может быть раньше даты рождения')
		return data

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = '__all__'