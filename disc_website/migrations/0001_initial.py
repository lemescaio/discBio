# Generated by Django 4.0.3 on 2022-06-28 01:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('ra', models.IntegerField(unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('aluno_empregado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Teste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('tipo', models.IntegerField(choices=[(1, 'check-box'), (2, 'radio-button')])),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.CharField(max_length=50)),
                ('ano', models.IntegerField()),
                ('semestre', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Universidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_ini', models.DateTimeField()),
                ('data_fim', models.DateTimeField()),
                ('influencia', models.FloatField()),
                ('dominancia', models.FloatField()),
                ('cautela', models.FloatField()),
                ('estabilidade', models.FloatField()),
                ('resultado_final', models.CharField(default='', max_length=255)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disc_website.aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enunciado', models.TextField(max_length=140)),
                ('teste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disc_website.teste')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('expire_date', models.DateTimeField()),
                ('apelido', models.CharField(max_length=150)),
                ('teste', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disc_website.teste')),
                ('universidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disc_website.universidade')),
            ],
        ),
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.CharField(max_length=140)),
                ('perfil', models.IntegerField(choices=[(1, 'dominancia'), (2, 'influencia'), (3, 'cautela'), (4, 'estabilidade')])),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='disc_website.pergunta')),
            ],
        ),
    ]

