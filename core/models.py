from django.db import models
from django.utils.text import slugify

class Specialite(models.Model):
    """Spécialités de l'ENISE (Génie Civil, Mécanique, Physique)"""
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    icone = models.CharField(max_length=50, blank=True, help_text="Classe FontAwesome, ex: fa-building")
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre', 'nom']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom

class Actualite(models.Model):
    """Actualités de l'école"""
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenu = models.TextField()
    image = models.ImageField(upload_to='actualites/', blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    est_publie = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_publication']
    
    def __str__(self):
        return self.titre

class Contact(models.Model):
    """Messages du formulaire de contact"""
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.nom} - {self.sujet}"

class Partenaire(models.Model):
    """Partenaires académiques et industriels"""
    nom = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='partenaires/')
    url = models.URLField(blank=True)
    type_partenaire = models.CharField(max_length=50, choices=[
        ('ACADEMIQUE', 'Académique'),
        ('INDUSTRIEL', 'Industriel'),
        ('INSTITUTIONNEL', 'Institutionnel'),
    ])
    
    def __str__(self):
        return self.nom

class Statistique(models.Model):
    """Statistiques affichées sur le site"""
    nom = models.CharField(max_length=100)
    valeur = models.CharField(max_length=50)
    suffixe = models.CharField(max_length=10, default='', blank=True)
    icone = models.CharField(max_length=50, help_text="Classe FontAwesome")
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return f"{self.nom}: {self.valeur}"
