from django.db import models
import csv

# Create your models here.
class Star(models.Model):
    """
    明星类，包括姓名、年龄、性别
    """
    name=models.CharField(max_length=64)
    age=models.IntegerField(null=True)
    sex = models.BooleanField(null=True)

    def __str__(self):
        return self.name

class StarRelationship(models.Model):
    """
    明星关系类,采用全手动来实现同一个类的多对多
    """
    relation = models.CharField(max_length=64)
    starA=models.ForeignKey(Star,on_delete=models.CASCADE,related_name='personA')
    starB=models.ForeignKey(Star,on_delete=models.CASCADE,related_name='personB')


class Location(models.Model):
    """
    地点类，包括地点名
    """
    location=models.CharField(max_length=64)

class Event(models.Model):
    """
    事件类，包括时间,事件与明星存在多对多的关系
    """
    year = models.IntegerField(null=True)
    place=models.CharField(max_length=64)
    event_title=models.CharField(max_length=64)
    star = models.ManyToManyField('Star')

class LocRelationship(models.Model):
    """
    地点与明星关系类，地点与明星是多对多的关系，但是想要新增一个关系属性，所以采用全手动建表
    """
    locrelation = models.CharField(max_length=64)
    loc = models.ForeignKey(Location, on_delete=models.CASCADE)
    star = models.ForeignKey(Star, on_delete=models.CASCADE)

