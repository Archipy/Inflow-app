# Generated by Django 4.1.2 on 2023-07-13 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manana', '0007_outs_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outs',
            name='hora',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Hora'),
        ),
    ]
