# Generated by Django 4.2.1 on 2023-05-25 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_email_verificado_trabajador_direccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='cliente', to='usuarios.direccion'),
        ),
    ]
