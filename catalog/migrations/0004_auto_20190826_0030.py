# Generated by Django 2.2.4 on 2019-08-25 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003b_reader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='biography',
            field=models.TextField(help_text='Введите краткую биографию автора', verbose_name='Краткая биография'),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(help_text='Введите дату рождения автора в формате ГГГГ-ММ-ДД', verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, help_text='Введите дату смерти автора в формате ГГГГ-ММ-ДД; поле необязательно', null=True, verbose_name='Дата смерти'),
        ),
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(help_text='Введите имя автора', max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(help_text='Введите фамилию автора', max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, help_text='Выберите автора из списка', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(help_text='Введите краткое описание книги', verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(help_text='Введите название книги', max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.IntegerField(help_text='Введите год написания книги', verbose_name='Год написания'),
        ),
    ]
