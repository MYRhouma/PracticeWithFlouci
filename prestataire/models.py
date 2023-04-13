import secrets

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from wallet.models import Wallet


# Create your models here.
CANDIDATURE_CHOICES = (
    (0,"Pending"),
    (1,"Accepted"),
    (2,"Rejected")
)
class CandidaturePrestataire(models.Model):
    username = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    message = models.TextField(max_length=2048)
    justificatif = models.ImageField(upload_to="pictures/justificatifs-candidature/",null=True)
    status = models.IntegerField(choices=CANDIDATURE_CHOICES, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username
class Prestataire(models.Model):
    # on peux ajouter un champ à choix multiple "Type" exemple : (electricien, plombier, coursier, autre ..)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet,null=True,blank=True,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CandidaturePrestataire)
def prestataire_creation(sender, instance, *args, **kwargs):
    if instance.status == 1 and User.objects.filter(username = instance.username).count()==0:
        password_length = 8
        password = secrets.token_urlsafe(password_length)
        print(password)
        user = User.objects.create_user(username=instance.username,
                                    first_name = instance.first_name,
                                    last_name = instance.last_name,
                                    password=password)
        wallet = Wallet.objects.create(user=user)
        Prestataire.objects.create(user=user,
                                    wallet=wallet,
                                    )
@receiver(post_delete,sender=Prestataire)
def delete_prestataire(sender,instance,*args,**kwargs):
    User.objects.get(id=instance.user.id).delete()

