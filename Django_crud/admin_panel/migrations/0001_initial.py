# Generated by Django 4.2.6 on 2023-12-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('address', models.TextField()),
                ('phone', models.IntegerField()),
            ],
        ),
    ]
