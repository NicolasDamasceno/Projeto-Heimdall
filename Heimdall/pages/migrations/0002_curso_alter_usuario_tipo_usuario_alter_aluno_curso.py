# Generated by Django 5.1.4 on 2025-01-17 14:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('turno', models.CharField(choices=[('manha', 'Manhã'), ('tarde', 'Tarde'), ('noite', 'Noite')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('AL', 'Aluno'), ('DC', 'Docente'), ('VT', 'Visitante')], default='AL', max_length=2),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pages.curso'),
        ),
    ]
