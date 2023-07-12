# 配置临时环境变量，只在代码运行时生效
import os
# 设置环境变量
os.environ['DJANGO_SETTINGS_MODULE']="star.settings"
# 导入django，同时初始化 Django 环境
import django; django.setup()
from starapp.models import Star, StarRelationship,Location,Event,LocRelationship

def qurey_test1():
    """
    查找出生地在香港的明星
    涉及跨表查询，名字是在Star表中，出生地信息是在LocRelationship表中
    """
    print("查询1:查找出生地在香港的明星")
    stars_from_hongkong = Star.objects.filter(locrelationship__locrelation='出生地',locrelationship__loc__location='香港')
    for star in stars_from_hongkong:
        print(star.name)

def query_test2():
    """
    查找涉及事件‘艳照门事件’中的明星的关系
    涉及跨表查询，事件的名称被存在Event表中，事件与明星的关系被存在Star_Event表中，明星之间的关系被存在StarRelationship中
    """
    print("查询2:查找涉及‘艳照门事件’中的明星之间的关系")
    event = Event.objects.get(event_title='艳照门事件')
    stars_in_event = event.star.all()

    star_relationships = StarRelationship.objects.filter(starA__in=stars_in_event, starB__in=stars_in_event)

    for relationship in star_relationships:
        print(relationship.starA.name, relationship.relation, relationship.starB.name)

if __name__ == '__main__':
    qurey_test1()
    query_test2()



