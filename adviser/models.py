from django.contrib.auth.models import User
from django.db import models
from django.core.files import File
import os
import urllib

# Create your models here.
class advisers(models.Model):
    adviser_name = models.CharField(max_length=50)
    photo_url = models.URLField(max_length=500)

    #this code apply if use media root with urls then it will store data in imagefield
    # photo = models.ImageField(upload_to = 'images')
    
    # def get_remote_image(self):
    #     if self.photo_url and not self.photo:
    #         result = urllib.urlretrieve(self.photo_url)
    #         self.photo.save(
    #             os.path.basename(self.photo_url),
    #             File(open(result[0]))
    #             )
    #         self.save()


class booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    adviser_appoint = models.ForeignKey(advisers,on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=False)
