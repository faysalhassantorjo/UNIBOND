# Generated by Django 4.2.6 on 2023-11-14 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_user_delete_customuser_alter_message_user_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='img',
            new_name='imgage',
        ),
    ]
