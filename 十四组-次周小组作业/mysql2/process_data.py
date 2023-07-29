# 配置临时环境变量，只在代码运行时生效
import os
# 设置环境变量
os.environ['DJANGO_SETTINGS_MODULE']="star.settings"
# 导入django，同时初始化 Django 环境
import django; django.setup()
from starapp.models import Star, StarRelationship,Location,Event,LocRelationship
from django.db.models import Q

def change_test1():
    """
    将王菲与谢霆锋的关系修改成“前男女友”（原来是“旧爱”）
    """
    print("测试1：修改两个明星之间的关系")
    # 查询王菲和谢霆锋的明星关系
    star_relationship = StarRelationship.objects.filter(
        Q(starA__name='王菲', starB__name='谢霆锋') | Q(starA__name='谢霆锋', starB__name='王菲')
    ).first()
    # 修改关系为"前男女友"
    if star_relationship:
        star_relationship.relation = '前男女友'
        star_relationship.save()
        print(f"王菲和谢霆锋的关系已修改为：{star_relationship.relation}")
    else:
        print("找不到王菲和谢霆锋之间的明星关系")


def delete_test2():
    """
    删除一个明星
    要把明星与明星关系，明星与地点关系，明星与事件关系，明星本身都删除
    """
    print("测试2:删除一个明星")
    star = Star.objects.get(name='朴树')
    # 删除明星关系
    StarRelationship.objects.filter(Q(starA=star) | Q(starB=star)).delete()
    # 解除明星与事件的关联
    star.event_set.clear()
    # 解除明星与地点的关联
    star.locrelationship_set.clear()
    # 删除明星
    star.delete()


if __name__ == '__main__':
    change_test1()
    delete_test2


