from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class reader(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # mobile = models.BigIntegerField(unique=True)
    regs_date = models.DateField(auto_now_add=True)
    gender = models.TextField(max_length=12)

    def __str__(self):
        if self.user.first_name:
            return str(self.user.first_name)+" "+str(self.user.last_name)
        else:
            return self.user.username
            

@receiver(post_save, sender=User)
def create_reader_profile(sender,instance,created,**kwargs):
    if created:
        reader.objects.create(user = instance)

@receiver(post_save,sender=User)
def reader_profile_save(sender,instance,**kwargs):
    instance.reader.save()

class contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=1000)
    def __str__(self):
        return self.name
    
