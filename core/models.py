from django.db import models
from django.contrib.auth.models import User


class Plataforma(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Motorista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username


class Corrida(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"{self.plataforma.nome} - R${self.valor}"


class Despesa(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"{self.descricao} - R${self.valor}"