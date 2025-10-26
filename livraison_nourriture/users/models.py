from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime


#Create your models here.

class CustomUser(AbstractUser):
    profils_list=[
        ('client',"Client"),
        ('entreprise','Entreprise'),
        ('livreur','Livreur'),
    ]
    tel=models.IntegerField()
    profile= models.CharField(max_length=15, choices=profils_list,default="client")
    username=models.CharField(max_length=100,blank=True,default="")
    email=models.EmailField(unique=True,max_length=190)
    code=models.CharField(max_length=10,blank=True,default="")
    a_restaurant=models.BooleanField(default=False)
    a_boutique = models.BooleanField(default=False)
    logo = CloudinaryField("image", blank=True, null=True, default='')
    quartier = models.CharField(max_length=100,default="",blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class HoraireHebdomadaire(models.Model):
    pass
class Horaire(models.Model):
    jours=[
        ('lundi','Lundi'),
        ('mardi','Mardi'),
        ("mercredi",'Mercredi'),
        ('jeudi','Jeudi'),
        ('vendredi','Vendredi'),
        ('samedi','Samedi'),
        ('dimanche','Dimanche')
    ]
    jour = models.CharField(max_length=15, choices=jours)
    horaire_hebdo = models.ForeignKey(HoraireHebdomadaire, on_delete=models.CASCADE, related_name="horaires")
    ouverture=models.TimeField(default=datetime.time(8,0))
    fermeture=models.TimeField(default=datetime.time(18,0))


class Restaurant(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="restaurant")
    type_plat=models.CharField(max_length=100)
    rate= models.FloatField(default=0.0)
    rating_count = models.FloatField(default=0.0)
    rating_sum = models.FloatField(default=0.0)
    est_ouvert=models.BooleanField(default=False)
    horaire=models.OneToOneField(HoraireHebdomadaire,on_delete=models.CASCADE,related_name="restaurant",null=True,default=None)
    def __str__(self):
        return f"{self.user.username}-{self.user.quartier}"

class Boutique(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="boutique")
    est_ouvert = models.BooleanField(default=False)
    couleur=models.CharField(max_length=10,default="#ffffff")
    rate = models.FloatField(default=0.0)
    rating_count = models.FloatField(default=0.0)
    rating_sum = models.FloatField(default=0.0)
    horaire= models.OneToOneField(HoraireHebdomadaire, on_delete=models.CASCADE, related_name="boutique",null=True,default=None)
    def __str__(self):
        return f"Boutique {self.user.username}"

class Livreur(models.Model):
    STATUT_LIST=[
        ("occupé","Occupé"),
        ('libre',"Libre"),
    ]
    matricule=models.CharField(max_length=30)
    description=models.TextField(blank="",default="")
    est_a_personne=models.BooleanField(default=False)
    entreprise=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="livreurs",null=True,default=None)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="livreur")
    statut=models.CharField(max_length=15, choices=STATUT_LIST,default="libre")
    rate = models.FloatField(default=0.0)
    rating_count = models.FloatField(default=0.0)
    rating_sum = models.FloatField(default=0.0)


