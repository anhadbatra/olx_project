# Generated by Django 2.1.5 on 2019-12-06 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20191206_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertise',
            name='date_created',
            field=models.DateField(null=True),
        ),
    ]
