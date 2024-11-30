from django.db import models


class Usuario(models.Model):
    NIVEL_USUARIO = [
        ( "Cliente" , "Cliente" ),
        ( "Administrador" , "Administrador" ),
     ]
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255, null=False, blank=False)
    email = models.CharField(max_length=255, unique=True)
    senha = models.CharField(max_length=255)

    nivel_usuario = models.CharField(max_length=15, choices=NIVEL_USUARIO, default="Cliente") # Adicionando o nível de conta

    def save(self, *args, **kwargs):
        if Usuario.objects.filter(nome=self.nome, email=self.email, senha=self.senha, nivel_usuario=self.nivel_usuario).exists():
            pass
        else:
            super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome
    

class Epis(models.Model):
    id_epi = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255, null=False, blank=False)
    quantidade = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome
    
class Acao(models.Model):
    STATUS_CHOICES = [
        ('emprestado', 'Emprestado'),
        ('devolvido', 'Devolvido'),
    ]
    
    nome_equipamento = models.ForeignKey(Epis, on_delete=models.CASCADE)  # Nome do equipamento
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relacionamento com o seu modelo Usuario
    data_emprestimo = models.DateTimeField()  # Data do empréstimo
    data_prevista_devolucao = models.DateTimeField()  # Data prevista para devolução
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='emprestado')  # Status do equipamento
    condicoes_emprestimo = models.TextField(null=True, blank=True)  # Condições do equipamento ao ser emprestado
    data_devolucao = models.DateTimeField(null=True, blank=True)  # Data real da devolução (pode ser nula)
    observacoes_devolucao = models.TextField(null=True, blank=True)  # Observações ao devolver o equipamento
    data_acao = models.DateTimeField(auto_now_add=True)  # Data de criação da ação (emprestimo ou devolução)
    
    def __str__(self):
        return f'{self.nome_equipamento} ({self.usuario.nome}) - {self.get_status_display()}'

    class Meta:
        verbose_name = 'Ação'
        verbose_name_plural = 'Ações'
        ordering = ['-data_acao']
