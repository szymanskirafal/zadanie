# Generated by Django 2.1.5 on 2019-01-08 13:24

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='entry',
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='entry',
            name='comments_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='entry',
            name='pub_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
