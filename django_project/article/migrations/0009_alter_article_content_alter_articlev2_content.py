# Generated by Django 4.2 on 2024-09-20 14:53

from django.db import migrations, models
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_alter_articlev2_options_alter_author_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='articlev2',
            name='content',
            field=mdeditor.fields.MDTextField(verbose_name='內容'),
        ),
    ]