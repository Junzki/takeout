# Generated by Django 4.2.2 on 2023-06-14 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0003_imageinput_alter_sample_identity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='alias_name',
        ),
    ]