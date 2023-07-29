import sys
from config import graph
sys.path.append('../')


def query(name):
    data = graph.run(
    "match(p )-[r]->(n:entity{name:'%s'}) return p.name, r.relation, n.name\
        Union all\
    match(p:entity {name:'%s'}) -[r]->(n) return p.name, r.relation, n.name"
        % (name, name)
    )  # 找出name涉及的所有name和关系
    data = list(data)
    print('query.data:',data)
    return get_json_data(data)


def get_json_data(data):
    json_data={'data':[],"links":[]}
    d=[]  # 涉及的name保存到d
    for i in data:
        d.append(i['p.name'])
        d.append(i['n.name'])
        d=list(set(d))
    print(d)

    name_dict={}
    count=0
    for j in d:
        j_array=j.split("_")  # 将当前name分割出来--每个list中有一个‘name’
        print(j_array)
        data_item={}
        name_dict[j_array[0]]=count  # 为这些name标号，存到字典name_dict里
        count+=1
        data_item['name']=j_array[0]  # data_item短暂存储'name'和name的对应关系，相当于temp
        json_data['data'].append(data_item)  # 将当前data_item加入json_data的data中
    print(name_dict)
    print(json_data)

    for i in data:
        link_item={}  # 与name_item功能类似，存储关系（用序号代替人名）
        link_item['source'] = name_dict[i['p.name']]
        link_item['target'] = name_dict[i['n.name']]
        link_item['value'] = i['r.relation']
        print(link_item)
        json_data['links'].append(link_item)

    print(json_data)
    return json_data


def get_KGQA_answer0(array):
    print('array', array)
    #
    # name=array[0]
    # print(name)
    # data = graph.run(
    #     "match(p)<-[r:%s{relation: '%s'}]-(n:Entity{Name:'%s'}) return  p.Name,n.Name,r.relation" % (
    #         array[1], array[1], name)  # 关系类型、关系属性、查询节点名字
    # )
    # print(data)
    # data = list(data)
    # print(data)

    data_array = []
    for i in range(1):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['p.name']
        data = graph.run(
            "match(p)<-[r:%s{relation: '%s'}]-(n:entity{name:'%s'}) return  p.name,n.name,r.relation" % (
                array[i + 1], array[i + 1], name)  # 关系类型、关系属性、查询节点名字
        )
        data = list(data)
        data_array.extend(data)
        # print("data", data)
        # print("==="*36)
    print("data_array",data_array)
    return data_array


def get_KGQA_answer1(array):
    print('array', array)

    data_array = []
    for i in range(1):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['p.name']
        data = graph.run(
            "MATCH (a)-[r]-(b) WHERE a.name = '%s' AND b.name = '%s' MATCH (a)-[r]-(b) RETURN a, r, b"
            %(array[0],array[1])
        )
        data = list(data)
        data_array.extend(data)
        # print("data", data)
        # print("==="*36)
    print("data_array",data_array)
    return data_array


def get_KGQA_answer2(array):
    print('array', array)

    data_array = []
    for i in range(1):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['p.name']
        data = graph.run(
            "MATCH (a)-[r]-(b) WHERE a.name = '哈利·波特' AND b.name = '乔治·韦斯莱' RETURN r"
        )
        data = list(data)
        data_array.extend(data)
        # print("data", data)
        # print("==="*36)
    print("data_array",data_array)
    return data_array


if __name__ == '__main__':

    # test1=['哈利·波特','侄女']
    # query(test1[0])
    # print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
    # test_array=get_KGQA_answer(test1)
    # print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
    # print(test_array)
    # get_json_data(test_array)

    test2=['哈利·波特', '乔治·韦斯莱']
    test_array2=get_KGQA_answer1(test2)
    print(test_array2[0])
    print(test_array2[1])


