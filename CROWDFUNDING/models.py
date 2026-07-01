from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    Photo=models.ImageField(upload_to="Images/", blank=True)
    is_contri=models.BooleanField(default=True)
    statut=models.CharField(default="CONTRIBUTEUR", max_length=100)
    compte=models.CharField(default="sb-qr7hu32116407@business.example.com", max_length=350)
    Dates=models.DateField(auto_now=True)
     # Autres champs personnalisés


class Types_Contributions(models.Model):
    users=models.CharField(default="-", max_length=200)
    type=models.CharField(max_length=100)
    
    def __str__(self):
        return self.type

class Types_Projets(models.Model):
    type=models.CharField(max_length=100)
    Description=models.TextField(max_length=700)
    Image=models.ImageField(upload_to="Images/",)
    def __str__(self):
        return self.type

class Projets(models.Model):
    Titre=models.CharField(max_length=150)
    Type=models.ForeignKey(Types_Projets, on_delete=models.CASCADE)
    Montant=models.DecimalField(max_digits=10, decimal_places=0)
    Utilisateur=models.CharField(max_length=150)
    Reste=models.DecimalField(max_digits=10, decimal_places=1, default=0)
    Description=models.TextField(max_length=700)
    Images=models.ImageField(upload_to="Images/")
    Date_du_début=models.DateField(auto_now=False)
    Date_de_fin=models.DateField(auto_now=False)
    Interet=models.DecimalField(max_digits=10, decimal_places=1)
    Commission=models.DecimalField(max_digits=10, decimal_places=2)
    compte=models.CharField(default="sb-qr7hu32116407@business.example.com", max_length=350)
    Echéance=models.DecimalField(max_digits=10, decimal_places=0, default=0)
    Contribution=models.DecimalField(max_digits=10, decimal_places=0, default=0)
    def __str__(self):
        return self.Titre
    

class Contributions(models.Model):
    Utilisateurs= models.CharField(max_length = 150)
    Projets=models.ForeignKey(Projets, on_delete=models.CASCADE)
    Type_Contributions=models.CharField(max_length=100, default="rien")
    Montant=models.DecimalField(max_digits=100, decimal_places=1)
    interet=models.DecimalField(max_digits=5, decimal_places=1)
    Remboursement=models.DecimalField(max_digits=100, decimal_places=1)
    compte=models.CharField(default="sb-qr7hu32116407@business.example.com", max_length=350)
    Dates=models.DateField(auto_now=True)
        
    def __str__(self):
        return f"{self.type}-{self.Montant}-{self.Dates}"
