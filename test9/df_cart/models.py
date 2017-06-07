from django.db import models

# Create your models here.


class CartInfo(models.Model):
    user = models.ForeignKey('users.userInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')
    count = models.IntegerField()