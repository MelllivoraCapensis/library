from django.contrib import admin
from .models import Author, Book, \
	Reader, Grade

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 
		'date_of_birth', 'date_of_death', 'image')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	readonly_fields = ('grades',)
	list_display = ('id', 'title', 'author', 
		'year', lambda obj: obj.description[:50] + '...', 'file', 'image')

	def grades(self, obj):
		grades = obj.grade_set.all()
		grade_list = 'Reader - Grade \n'
		for g in grades:
			grade_list += f' {g.reader} - {g.value} \n'
		return grade_list



@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
	fields = ['user', 'books']
	list_display = ('user', 'get_books')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
	list_display = ('reader', 'book', 'value')