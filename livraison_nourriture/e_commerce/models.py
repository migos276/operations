from django.db import models

from users.models import Restaurant
from cloudinary.models import CloudinaryField
import datetime
# Create your models here.


class Restaurant_Plat(models.Model):
    plat=models.ForeignKey("Plat", on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    rate=models.FloatField(default=0.0)
    is_avialable=models.BooleanField(default=True)
    rating_count=models.FloatField(default=0.0)
    rating_sum=models.FloatField(default=0.0)
    image = CloudinaryField("image", blank=True, null=True, default='')
    class Meta:
        unique_together=("restaurant","plat")

class Plat(models.Model):
    nom = models.CharField(max_length=70)
    restaurants=models.ManyToManyField(Restaurant,through=Restaurant_Plat,related_name="plats")

    def __str__(self):
        return self.nom

class Menu_Plat(models.Model):
    plat=models.ForeignKey(Restaurant_Plat, on_delete=models.CASCADE)
    description=models.TextField(blank=True,default='aucune description')
    menu=models.ForeignKey("Menu",on_delete=models.CASCADE,related_name="menu_plat",null=True,default=None)
    prix=models.IntegerField()

class Menu(models.Model):
    jours=[
        ('lundi','Lundi'),
        ('mardi','Mardi'),
        ("mercredi",'Mercredi'),
        ('jeudi','Jeudi'),
        ('vendredi','Vendredi'),
        ('samedi','Samedi'),
        ('dimanche','Dimanche')
    ]
    plats=models.ManyToManyField(Restaurant_Plat,through=Menu_Plat,related_name="menus")
    jour = models.CharField(max_length=15, choices=jours)
    menu_hebdo = models.ForeignKey("MenuHebdomadaire", on_delete=models.CASCADE, related_name="menus")

    class Meta:
        unique_together=()
        constraints=[
            models.UniqueConstraint(fields=['menu_hebdo','jour'],name="unique_menuhebdo_jour")
        ]

class MenuHebdomadaire(models.Model):
    restaurant=models.OneToOneField(Restaurant,on_delete=models.CASCADE,related_name="menu_hebdo")
class MenuStatique(models.Model):
    restaurant=models.OneToOneField(Restaurant,on_delete=models.CASCADE,related_name="menu_statique")

class MenuStatique_Plat(models.Model):
    plat=models.ForeignKey(Restaurant_Plat, on_delete=models.CASCADE)
    description=models.TextField(blank=True,default='aucune description')
    prix=models.IntegerField()
    menu= models.ForeignKey("MenuStatique", on_delete=models.CASCADE, related_name="plats",default=1)
