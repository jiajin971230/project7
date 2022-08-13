from django.db import models
from datetime import datetime
#模型管理器
class ModelManager(models.Manager):
    def get_queryset(self):
        return super(ModelManager,self).get_queryset().filter(is_valid=1)
#用户模型
class User(models.Model):
    username=models.CharField(max_length=20,db_column='user_name')
    password=models.CharField(max_length=100)
    truename=models.CharField(max_length=20,null=True, db_column='true_name')
    email=models.CharField(max_length=30)
    phone=models.CharField(max_length=20,null=True)
    is_valid=models.IntegerField(default=1)
    creat_time=models.DateTimeField(default=datetime.now().date())
    update_date=models.DateTimeField(null=True)
    code=models.CharField(max_length=255,null=True)
    status=models.IntegerField(default=0)
    timestamp=models.CharField(max_length=255,null=True)

    objects=ModelManager()
    #元信息
    class Meta(object):
        db_table='t_user'


