from rest_framework.serializers import ModelSerializer
from ..models import Author, Book

class AuthorSerializer(ModelSerializer):
	class Meta:
		model = Author
		fields = '__all__'

class BookSerializer(ModelSerializer):
	class Meta:
		model = Author
		fields = '__all__'