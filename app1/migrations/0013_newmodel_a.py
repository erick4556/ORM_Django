# Generated by Django 3.2.7 on 2021-09-28 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_newmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='newmodel',
            name='a',
            field=models.CharField(db_column='another_name', default='', max_length=50),
        ),
    ]
