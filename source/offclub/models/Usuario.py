from offclub.models import *
class Usuario(models.Model):
    nomeUsuario = models.CharField(null=False, max_length=200)
    logradouro = models.CharField(null=False, max_length=200)
    estado = models.CharField(null=False, max_length=2)
    bairro = models.CharField(null=False, max_length=200)
    complemento = models.CharField(null=False, max_length=130)
    cidade = models.CharField(null=False, max_length=100)
    numero = models.CharField(null=False, max_length=8)
    razaoSocial = models.CharField(null=True, max_length=80)
    cnpj = models.CharField(null=True, max_length=15)
    descricao = models.CharField(null=True, max_length=200)
    cpf = models.CharField(null=True, max_length=11)
    dataNascimento = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
       return '{}'.format(self. nomeUsuario)