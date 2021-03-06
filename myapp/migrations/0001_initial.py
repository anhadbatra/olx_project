# Generated by Django 2.2.7 on 2019-11-19 10:02

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
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=30, null=True)),
                ('current_user', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'categorie',
                'db_table': 'category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('subject', models.CharField(max_length=200, null=True)),
                ('message', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'db_table': 'contact',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(blank=True, max_length=30, null=True)),
                ('current_user', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Location',
                'db_table': 'location',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Detail',
                'db_table': 'user_detail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Advertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(max_length=300)),
                ('image', models.FileField(blank=True, help_text='Upload only .png, .jpg & .jpeg image extension.', null=True, upload_to='image/ad_image')),
                ('contact', models.BigIntegerField()),
                ('price', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Category')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Location')),
            ],
            options={
                'verbose_name_plural': 'Advertise',
                'db_table': 'advertise',
                'managed': True,
            },
        ),
    ]
