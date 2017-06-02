from django.db import models

# Create your models here.


class userInfo(models.Model):
    username = models.CharField(max_length=20)
    passwd = models.CharField(max_length=40)
    umail = models.CharField(max_length=40)
    utel = models.CharField(max_length=15, default='')
    upost = models.CharField(max_length=11, default='')
    uaddress = models.CharField(max_length=40, default='')
    ushou = models.CharField(max_length=40,default='')



