# Generated by Django 4.2.16 on 2024-10-19 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_cadastro_usuarios', '0007_alter_usuario_nivel_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_equipamento', models.CharField(max_length=100)),
                ('data_emprestimo', models.DateTimeField()),
                ('data_prevista_devolucao', models.DateTimeField()),
                ('status', models.CharField(choices=[('emprestado', 'Emprestado'), ('devolvido', 'Devolvido')], default='emprestado', max_length=10)),
                ('condicoes_emprestimo', models.TextField(blank=True, null=True)),
                ('data_devolucao', models.DateTimeField(blank=True, null=True)),
                ('observacoes_devolucao', models.TextField(blank=True, null=True)),
                ('data_acao', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_cadastro_usuarios.usuario')),
            ],
            options={
                'verbose_name': 'Ação',
                'verbose_name_plural': 'Ações',
                'ordering': ['-data_acao'],
            },
        ),
    ]