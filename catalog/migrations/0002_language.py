# Generated by Django 4.0 on 2021-12-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a language (e.h. English)', max_length=200)),
            ],
        ),
    ]
