# Generated by Django 4.1.2 on 2022-11-09 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_software_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='update',
            field=models.CharField(default='not', max_length=50),
        ),
    ]
