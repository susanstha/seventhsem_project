# Generated by Django 2.1.7 on 2019-08-10 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_auto_20190810_1156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-hit_count_generic__hits']},
        ),
    ]
