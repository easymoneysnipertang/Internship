import pymysql
from config import config
def create_table():
    """
    功能; 使用sql语句查询数据库中人员身份信息.
    参数: sql(string)
    """
    db = pymysql.connect(host='localhost', user='root', password=config['MYSQL_PASSWORD'], database=config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()
    try:
        sql="""
drop table if exists Affiliation;
drop table if exists participate_in;
drop table if exists situation;
drop table if exists event;
drop table if exists star;
drop table if exists star_relationship;

/*==============================================================*/
/* Table: Affiliation                                           */
/*==============================================================*/
create table Affiliation
( Affiliation_id       int not null auto_increment,
   situation_id         int not null,
   star_id              int not null,
   connection         varchar(10) not null,
   primary key (Affiliation_id)
);

/*==============================================================*/
/* Table: event                                                 */
/*==============================================================*/
create table event
(
   event_id             int not null auto_increment,
   event_name           varchar(50) not null,
   event_time           year not null,
   event_situation      varchar(10) not null,
   primary key (event_id)
);

/*==============================================================*/
/* Table: participate_in                                        */
/*==============================================================*/
create table participate_in
(
   star_id              int not null,
   event_id             int not null,
   primary key (star_id, event_id)
);

/*==============================================================*/
/* Table: situation                                             */
/*==============================================================*/
create table situation
(
   situation_id         int not null auto_increment,
   situation_name       varchar(10) not null,
   primary key (situation_id)
);

/*==============================================================*/
/* Table: star                                                  */
/*==============================================================*/
create table star
(
   star_id              int not null auto_increment,
   star_age             int not null,
   star_gender          bool,
	 star_name            varchar(10) not null,
   primary key (star_id)
);

/*==============================================================*/
/* Table: star_relationship                                     */
/*==============================================================*/
create table star_relationship
(
   star_id              int not null,
   sta_star_id          int not null,
   relationship_content varchar(10) not null,
   primary key (star_id, sta_star_id)
);

alter table Affiliation add constraint FK_Affiliation foreign key (situation_id)
      references situation (situation_id) on delete restrict on update restrict;

alter table Affiliation add constraint FK_Affiliation2 foreign key (star_id)
      references star (star_id) on delete restrict on update restrict;

alter table participate_in add constraint FK_participate_in foreign key (star_id)
      references star (star_id) on delete restrict on update restrict;

alter table participate_in add constraint FK_participate_in2 foreign key (event_id)
      references event (event_id) on delete restrict on update restrict;

alter table star_relationship add constraint FK_star_relationship foreign key (star_id)
      references star (star_id) on delete restrict on update restrict;

alter table star_relationship add constraint FK_star_relationship2 foreign key (sta_star_id)
      references star (star_id) on delete restrict on update restrict;


        """
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        print('create success')
    except:
        print('create success')
        db.rollback()
    cur.close()
    db.close()
    return result


def query(sql):
    """
    功能; 使用sql语句查询数据库中人员身份信息.
    参数: sql(string)
    """
    db = pymysql.connect(host='localhost', user='root', password=config['MYSQL_PASSWORD'], database=config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()

        db.commit()

        print('query success')

    except:
        print('query loss')
        db.rollback()
    cur.close()
    db.close()
    return result


def delete(sql):
    """
    功能; 使用sql语句删除数据库中人员身份信息.
    参数: sql(string)
    """
    db = pymysql.connect(host='localhost', user='root', password=config['MYSQL_PASSWORD'], database=config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()
        print('delete success')
    except:
        print('delete loss')
        db.rollback()
    cur.close()
    db.close()

def add(sql):
    """
    功能; 使用sql语句添加数据库中人员身份信息.
    参数: sql(string)
    """
    db = pymysql.connect(host='localhost', user='root', password=config['MYSQL_PASSWORD'], database=config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()

        db.commit()
        result=1
        print('add success')

    except:
        result=0
        print('add loss')
        db.rollback()
    cur.close()
    db.close()
