# Generated by Django 2.2.4 on 2019-08-12 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='task_description',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
