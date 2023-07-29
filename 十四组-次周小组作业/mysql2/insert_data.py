# 配置临时环境变量，只在代码运行时生效
import os
# 设置环境变量
os.environ['DJANGO_SETTINGS_MODULE']="star.settings"
# 导入django，同时初始化 Django 环境
import django; django.setup()
from starapp.models import Star, StarRelationship,Location,Event,LocRelationship


"""
通过csv将数据导入到各个数据表中
"""
def import_data_from_csv_star(file_path):
    """
    Star明星表导入
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行

        for row in reader:
            # 解析CSV行数据
            name = row[0]
            age = row[1]
            sex = row[2]

            # 创建数据库对象并保存到 Star
            obj = Star(name=name, age=age,sex=sex)
            obj.save()

def import_data_from_csv_event(file_path):
    """
    Event事件表导入
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行

        for row in reader:
            # 解析CSV行数据
            year = row[0]
            place = row[1]
            event_title = row[2]

            # 创建数据库对象并保存到 Event
            obj = Event(year=year,place=place,event_title=event_title)
            obj.save()

def import_data_from_csv_location(file_path):
    """
    location地点表导入
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行

        for row in reader:
            # 解析CSV行数据
            location = row[0]

            # 创建数据库对象并保存到 Location
            obj = Location(location=location)
            obj.save()

def import_data_from_csv_starrelationship(file_path):
    """
    starrelationship明星与明星关系表导入
    多对多
    先get到两个明星对应的Star
    再创建StarRelationship，进行save
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行

        for row in reader:
            # 解析CSV行数据
            relation = row[0]
            stara = row[1]
            starb = row[2]

            a=Star.objects.get(name=stara)
            b=Star.objects.get(name=starb)

            # 创建数据库对象并保存到 StarRelationship
            obj = StarRelationship(relation=relation,starA=a,starB=b)
            obj.save()

def import_data_from_csv_locrelationship(file_path):
    """
    LocRelationship明星与地点关系导入
    多对多
    先get到地点名对应的Location和明星名对应的Star
    再创建LocRelationship，进行save
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行

        for row in reader:
            # 解析CSV行数据
            locrelation = row[0]
            loc_name = row[1]
            star_name = row[2]

            loc=Star.objects.get(name=loc_name)
            star=Star.objects.get(name=star_name)

            # 创建数据库对象并保存到 LocRelationship
            obj = LocRelationship(locrelation=locrelation,loc=loc,star=star)
            obj.save()

def import_data_from_csv_eventstar(file_path):
    """
    event_star明星与事件关系导入
    多对多，manyTomany
    """
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行

        for row in reader:
            # 解析CSV行数据
            star_name = row[0]
            event_name = row[1]

            # 查找或创建明星对象
            star, created = Star.objects.get_or_create(name=star_name)

            # 查找或创建事件对象
            event, created = Event.objects.get_or_create(name=event_name)

            # 添加ManyToMany关系
            star.events.add(event)  # 或者 event.stars.add(star)

if __name__ == '__main__':
    file_path_star = 'D:/University/star.csv'
    file_path_event = 'D:/University/event.csv'
    file_path_location = 'D:/University/location.csv'
    file_path_starrelationship = 'D:/University/starrelationship.csv'
    file_path_locrelationship = 'D:/University/locrelationship.csv'
    file_path_eventstar = 'D:/University//eventstar.csv'

    import_data_from_csv_star(file_path_star)
    import_data_from_csv_event(file_path_event)
    import_data_from_csv_location(file_path_location)
    import_data_from_csv_starrelationship(file_path_starrelationship)
    import_data_from_csv_locrelationship(file_path_locrelationship)
    import_data_from_csv_eventstar(file_path_eventstar)

