# Generated by Django 4.2.1 on 2023-05-23 01:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='email_verificado',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('primer_apellido', models.CharField(max_length=50)),
                ('segundo_apellido', models.CharField(max_length=50, null=True)),
                ('telefono', models.CharField(max_length=12)),
                ('tipo_trabajador', models.IntegerField(
                    choices=[(1, 'Administrador'), (2, 'Staff')])),
                ('usuario', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=120)),
                ('numero', models.CharField(max_length=5)),
                ('departamento', models.CharField(max_length=5, null=True)),
                ('codigo_postal', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=15)),
                ('descripcion', models.CharField(max_length=100)),
                ('comuna', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='gestion.comuna')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('primer_apellido', models.CharField(max_length=50)),
                ('segundo_apellido', models.CharField(max_length=50, null=True)),
                ('telefono', models.CharField(max_length=12)),
                ('direccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='cliente', to='usuarios.direccion')),
                ('forma_pago', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion.formapago')),
                ('usuario', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
