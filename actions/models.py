from django.db import models
from myuser.models import MyUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Action(models.Model):
    user = models.ForeignKey(MyUser,related_name='action',on_delete=models.CASCADE)
    act = models.CharField(max_length=125)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType , related_name='target_obj',blank=True,null=True,on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(blank=True , null=True)
    target = GenericForeignKey('target_ct','target_id')
    
    class Meta:
        ordering = ['created',]