# Generated by Django 4.0 on 2021-12-28 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_author_options_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_add_author', 'Can add author'),)},
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': (('can_add_book', 'Can add book'),)},
        ),
    ]
