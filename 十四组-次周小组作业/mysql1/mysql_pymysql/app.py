from flask import Flask, render_template, request, flash,  jsonify, redirect, url_for, session
from datetime import datetime, date
import query
# 创建flask对象
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gsolvit'


@app.route('/')
def head_html():
    return render_template('host.html')


@app.route('/user/logout')
def user_logout():
    return 'byebye!'


@app.route('/star/list')
def star_list():
    return render_template('star_list.html')

@app.route('/order/listJson')
def get_orders_star():
    name=request.args.get('star_name')
    print(name)
    categories=['star_id','star_name','star_age','star_gender','star_birth','star_country']
    data=[]
    if(name==None):
        sql = """
        select s1.star_id,s1.star_name,s1.star_age,s1.star_gender,t2.situation_name as'star_birth',t1.situation_name as'star_country'
from star s1,affiliation a1,affiliation a2,situation t1,situation t2
where s1.star_id=a1.star_id and a1.connection='国籍'
and s1.star_id=a2.star_id and a2.connection='出生地'
and t1.situation_id=a1.situation_id and t2.situation_id=a2.situation_id;
        """

        result = query.query(sql)
        print(result)
        for record in result:
            d = {categories[i]: record[i] for i in range(len(categories))}
            data.append(d)
        # print(data)
        data_dict = dict(code=0, msg="", count=1000, data=data)
    else:
        sql = """
                select s1.star_id,s1.star_name,s1.star_age,s1.star_gender,t2.situation_name as'star_birth',t1.situation_name as'star_country'
        from star s1,affiliation a1,affiliation a2,situation t1,situation t2
        where s1.star_id=a1.star_id and a1.connection='国籍'
        and s1.star_id=a2.star_id and a2.connection='出生地'
        and t1.situation_id=a1.situation_id and t2.situation_id=a2.situation_id
        and s1.star_name='%s';
                """%(name)
        #sql="select * from star where star_name='%s'"%(name)
        result = query.query(sql)
        for record in result:
            d = {categories[i]: record[i] for i in range(len(categories))}
            data.append(d)
        # print(data)
        data_dict = dict(code=0, msg="", count=1000, data=data)
    return jsonify(data_dict)

#相关关系详情表
@app.route('/relationship')
def relationship_list():
    id=request.args.get('star_id')
    sql="""
    select star.star_name,star_relationship.relationship_content
from star,star_relationship
where star.star_id=star_relationship.star_id
and star_relationship.sta_star_id='%s';
    """%(id)
    result=query.query(sql)
    categories=['related_star','relation']
    data=[]
    for record in result:
        d = {categories[i]: record[i] for i in range(len(categories))}
        data.append(d)
    print(data)
    return render_template('star_relation.html',data=data)


#创建事件表
@app.route('/event/list')
def event_list():
    return render_template('event_list.html')


@app.route('/order/eventlist')
def get_orders_event():
    sql1="""select * from event;"""
    categories=['event_id','event_name','event_time','event_situation','event_people']
    data=[]
    result = query.query(sql1)
    print(result)
    for record in result:
        d = {categories[i]: record[i] for i in range(len(categories)-1)}
        sql2="""select star.star_name from participate_in,star 
        where participate_in.star_id=star.star_id and participate_in.event_id='%s'"""%(record[0])
        result_names = query.query(sql2)
        s = ""
        for i, result_name in enumerate(result_names):
            s += result_name[0]
            if i < len(result_names) - 1:
                s += ","
        d['event_people']=s
        data.append(d)
    # print(data)
    data_dict = dict(code=0, msg="", count=1000, data=data)
    return jsonify(data_dict)

@app.route('/order/delete',methods=['GET'])
def event_delete():
    event_id=request.args.get('event_id')
    sql1="DELETE FROM participate_in where event_id='%s';"%(event_id)
    query.delete(sql1)
    sql2="DELETE FROM event where event_id='%s';"%(event_id)
    query.delete(sql2)
    return jsonify({'success': 1})

@app.route('/order/add')
def event_add():
    return render_template('event_add.html')

@app.route('/order/save',methods=['POST'])
def event_newsave():
    name=request.form.get('event_name')
    time=request.form.get('event_time')
    situation=request.form.get('event_situation')
    stars=request.form.get('event_stars')
    sql="INSERT INTO event(event_name,event_time,event_situation) VALUES('%s','%s','%s')"%(name,time,situation)
    query.add(sql)
    sql1="SELECT event_id from event where event_name='%s'and event_time='%s' and event_situation='%s'"%(name,time,situation)
    result1=query.query(sql1)
    result_event_id=result1[0][0]
    stars_list=stars.split("，")
    print(stars_list)
    for star in stars_list:
        sql2="select star_id from star where star_name='%s'"%(star)
        result2=query.query(sql2)
        print(len(result2))
        if len(result2)==0:
            print("OVER")
            response_data = {'success': 0}
            return jsonify(response_data)
        result_star_id=result2[0][0]
        print(result_star_id,result_event_id)
        sql3="INSERT INTO participate_in(star_id,event_id) VALUES(%s,%s)"%(result_star_id,result_event_id)
        query.add(sql3)
    response_data = {'success': 1}
    return jsonify(response_data)


if __name__ == '__main__':
    app.run()
