from django.db import models

class Paiement(models.Model):
    numero = models.CharField(max_length=20)
    montant = models.FloatField()
    status = models.CharField(max_length=20, default="en_attente")  # en_attente, succes, echec
    reference = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.numero} - {self.montant} ({self.status})"
