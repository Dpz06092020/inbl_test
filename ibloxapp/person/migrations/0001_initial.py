# Generated by Django 3.1 on 2020-09-03 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('enabled', models.BooleanField()),
                ('guid', models.UUIDField()),
            ],
            options={
                'db_table': 'person_data',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='person.persondata')),
            ],
            options={
                'db_table': 'person',
            },
        ),
    ]
