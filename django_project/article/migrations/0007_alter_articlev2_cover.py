# Generated by Django 4.2 on 2024-09-16 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_rename_cover_name_articlev2_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlev2',
            name='cover',
            field=models.ImageField(null=True, upload_to='static/images/cover_image'),
        ),
    ]