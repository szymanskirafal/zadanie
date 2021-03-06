# Generated by Django 2.1.5 on 2019-02-20 21:44

from django.db import migrations, models
import utilities.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('body', models.TextField(default='some text', max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('pub_date', models.DateTimeField(default=utilities.utilities.hundred_years_from_now)),
                ('comments_count', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Entries',
                'ordering': ['-modified'],
            },
        ),
    ]
