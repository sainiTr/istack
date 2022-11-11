# Generated by Django 4.1.2 on 2022-11-07 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('version', models.CharField(max_length=40)),
                ('icon', models.ImageField(upload_to='icons')),
                ('file', models.FileField(upload_to='exefile')),
                ('screenshots', models.ImageField(upload_to='scre')),
                ('descriptions', models.TextField()),
                ('rating', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=15)),
                ('count', models.IntegerField()),
                ('publisher', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('reldate', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
                ('installation', models.CharField(max_length=100)),
                ('info', models.CharField(max_length=120)),
                ('language', models.CharField(max_length=20)),
                ('pubinfo', models.CharField(max_length=150)),
            ],
        ),
    ]