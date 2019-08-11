# Generated by Django 2.2.4 on 2019-08-10 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100)),
                ('task_description', models.CharField(max_length=100)),
                ('task_priority', models.IntegerField(choices=[(1, 'High Priority'), (2, 'Medium Priority'), (3, 'Low Priority')], default=2)),
                ('task_status', models.IntegerField(choices=[(1, 'Not started'), (2, 'In progress'), (3, 'Done')], default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
