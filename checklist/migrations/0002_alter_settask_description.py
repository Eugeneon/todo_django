# Generated by Django 4.2.1 on 2023-10-17 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settask',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
