# Generated by Django 4.2.6 on 2023-11-14 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_message_user_alter_room_host_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='currently_studying',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
