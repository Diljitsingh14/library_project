from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from reader.models import reader
from django.contrib.auth.models import User


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def get_user_image_folder(instance, filename):
    return "%s/%s" %(instance.user.username, filename)
# Create your models here.


 

class book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,default='')
    # pdf_location = models.CharField(max_length=200,default='')
    thumbnail = models.CharField(max_length=200,default='',unique=True)
    file_book = models.FileField(upload_to="documents/%Y/%m%d", validators=[validate_file_extension],default='',unique=True,null=False)
    # thumbnail = models.FileField(upload_to="documents/%Y/%m%d", validators=[validate_file_extension],default='')
    date = models.DateField(auto_now_add=True)
    auther = models.CharField(max_length=100,default="admin")
    shell = models.ForeignKey('shells',on_delete=models.CASCADE,default='')
    upload_by = models.ForeignKey(reader,on_delete=models.CASCADE,default=1)
    likes = models.ManyToManyField(User,related_name="likes",blank=True)
    privacy =  models.BooleanField(default=False)
    def __str__(self):
        return self.name

    def likes_count(self):
        return self.likes.all().count()
    def is_liked(self,uid=0):
        if uid == 0:
            return False
        else:
            u = User.objects.get(id=uid)
            l = self.likes.filter(username=u.username).count()
            if l == 1:
                return True
            else:
                return False
         
            

class shells(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default ='',unique=True)
    upload_by = models.ForeignKey(reader,on_delete=models.CASCADE,default=1)
    privacy =  models.BooleanField(default=False)
    contrib =  models.BooleanField(default=True)
    create_on = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

@receiver(post_delete, sender=book)
def submission_delete(sender, instance, **kwargs):
    instance.file_book.delete(False) 


class reading_record(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey('book',on_delete=models.CASCADE)
    reader = models.ForeignKey(reader,on_delete=models.CASCADE)
    last_read_page = models.IntegerField()
    last_reading_date = models.DateField(auto_now_add=True)
    last_reading_time = models.TimeField(auto_now_add=True)
    total_page = models.IntegerField(default=0)
    class Meta:
        unique_together = ('book','reader')
    def __str__(self):
        return str(self.book.name[:5])+".. ("+str(self.reader)+") "+str(self.last_read_page)   
    def progress(self):
        t = self.last_read_page/self.total_page
        t = t*100;
        return t; 
    
