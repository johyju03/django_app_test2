# Generated by Django 2.2.6 on 2019-10-04 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stuck',
            new_name='stock',
        ),
    ]
