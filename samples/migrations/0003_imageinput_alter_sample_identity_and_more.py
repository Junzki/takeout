# Generated by Django 4.2.2 on 2023-06-14 14:51

from django.db import migrations, models
import pathlib
import samples.models


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0002_auto_20201213_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, null=True, upload_to=pathlib.PureWindowsPath('D:/Werkzeug/takeout/media/uploads'), verbose_name='Input File')),
                ('image_hash', models.CharField(default=None, max_length=128, null=True, verbose_name='Sample File HMAC-SHA256')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
        ),
        migrations.AlterField(
            model_name='sample',
            name='identity',
            field=models.CharField(default=samples.models.build_identity, max_length=255, verbose_name='Identity Key'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='sample_file',
            field=models.ImageField(default=None, null=True, upload_to=pathlib.PureWindowsPath('D:/Werkzeug/takeout/media/samples'), verbose_name='Sample File'),
        ),
    ]
