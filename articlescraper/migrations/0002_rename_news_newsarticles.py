# Generated by Django 4.0.5 on 2022-08-23 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articlescraper', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='News',
            new_name='NewsArticles',
        ),
    ]