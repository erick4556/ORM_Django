# Generated by Django 3.2.7 on 2021-10-01 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_crea', models.DateTimeField(auto_now_add=True)),
                ('date_updat', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=8)),
                ('active', models.BooleanField(default=True)),
                ('question_text', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_crea', models.DateTimeField(auto_now_add=True)),
                ('date_updat', models.DateTimeField(auto_now=True)),
                ('state', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=8)),
                ('active', models.BooleanField(default=True)),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.question')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]