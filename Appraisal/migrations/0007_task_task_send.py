# Generated by Django 5.0.7 on 2024-07-15 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appraisal', '0006_task_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_send',
            field=models.BooleanField(default=False),
        ),
    ]
