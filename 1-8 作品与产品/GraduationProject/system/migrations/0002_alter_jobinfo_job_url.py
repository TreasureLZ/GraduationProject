# Generated by Django 3.2.5 on 2022-01-03 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobinfo',
            name='job_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
