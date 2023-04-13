from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

TRANSACTION_STATUS=(
    (0,'Pending'),
    (1,'Approved'),
    (2,'Refused'),

)
class Wallet(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    def __str__(self):
        return self.user.username +' | '+ str(self.balance)+' dt'



class Transaction(models.Model):
    sender = models.ForeignKey(Wallet,on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Wallet,on_delete=models.CASCADE, related_name="receiver")
    amount = models.FloatField()
    status = models.IntegerField(choices=TRANSACTION_STATUS,default=0)
    def __str__(self):
        return self.sender.user.username + ' | '+self.receiver.user.username+' | '+str(self.amount)+" dt"

@receiver(post_save, sender=Transaction)
def transaction_creation(sender, instance, *args, **kwargs):
    if instance.status == 0:
        if instance.sender.balance >= instance.amount:
            instance.sender.balance-=instance.amount
            instance.sender.save()
            instance.receiver.balance += instance.amount
            instance.receiver.save()
            instance.status=1
        else:
            instance.status=2
        instance.save()
