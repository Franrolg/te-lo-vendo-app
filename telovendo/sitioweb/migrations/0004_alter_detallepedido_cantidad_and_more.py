# Generated by Django 4.2.1 on 2023-06-01 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitioweb', '0003_alter_detallepedido_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedido',
            name='cantidad',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='precio',
            field=models.IntegerField(),
        ),
    ]
