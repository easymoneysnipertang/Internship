import json
from py2neo import *
from kgqa.ltp import *

# 连接数据库
graph = Graph('bolt: // localhost:7687', auth=('neo4j', '12345678'))
main_role = ['哈利·波特', '赫敏·格兰杰', '罗恩·韦斯莱']
taged_names = ['鲁伯·海格', '乔治·韦斯莱', '弗雷德·韦斯莱', '阿不思·邓布利多', '米勒娃·麦格', '伊索特·塞耶', '霍格沃茨魔法学校'
               '德拉科·马尔福', '卢修斯·马尔福', '沃尔布加·布莱克', '魔法部', '英国魔法部', '美国魔法国会', '小天狼星·布莱克',
               '卢娜·洛夫古德', '多洛雷斯·乌姆里奇', '鼻涕虫俱乐部', '邓布利多军', '格兰芬多学院', '格兰芬多', '拉文克劳学院',
               '拉文克劳', '赫奇帕奇学院', '赫奇帕奇', '斯莱特林学院', '斯莱特林', '哈利·波特', '赫敏·格兰杰', '罗恩·韦斯莱']


def question1(value):  # 根据一个名搜索相关节点
    # 定义数据数组存储节点信息
    datas = []
    # 定义links数组存储关系信息
    links = []
    # 查询节点是否存在
    node = graph.run('MATCH(n{name:"' + value + '"}) return n').data()
    # 如果节点存在 len(node) 的值为 1，不存在的话 len(node) 的值为 0
    if len(node):
        # 如果该节点存在将该节点存入datas数组中
        # 构造字典存放节点信息
        dict_node = {
            'name': value,
            'symbolSize': 50,
            'category': 'center'
        }
        datas.append(dict_node)
        # 查询与该节点有关的节点，无向，步长为1，并返回这些节点
        # distinct!!! 数据集有些问题，需要distinct去重！
        nodes = graph.run('MATCH(n{name:"' + value + '"})<-->(m) return distinct m').data()
        # 处理节点信息
        for n in nodes:
            # 将节点信息的格式转化为 json
            node = json.dumps(n, ensure_ascii=False)
            node = json.loads(node)
            # 取出节点信息中的 name,label
            name = str(node['m']['name'])
            label = str(node['m']['label'])
            # 构造字典存放单个节点信息
            dict_node = {
                'name': name,
                'symbolSize': 50,
                'category': label
            }
            # 将单个节点信息存储进data数组中
            datas.append(dict_node)
        # 查询该节点所涉及的所有 relationship，无向，步长为 1，并返回
        reps = graph.run('MATCH(n{name:"' + value + '"})<-[rel]->(m) return rel').data()
        for r in reps:
            source = str(r['rel'].start_node['name'])
            target = str(r['rel'].end_node['name'])
            name = str(type(r['rel']).__name__)
            dict_node = {
                'source': source,
                'target': target,
                'name': name
            }
            links.append(dict_node)
        # 构造字典存储 datas 和 links
        search_neo4j_data = {
            'data': datas,
            'links': links
        }
        # 转化为 json 格式
        search_neo4j_data = json.dumps(search_neo4j_data)
        return search_neo4j_data
    else:
        print("查无此节点")
        return 0


def question3(value):  # 根据两个节点搜索其间关系
    # 定义数据数组存储节点信息
    datas = []
    # 定义links数组存储关系信息
    links = []
    # 查询节点是否存在
    # 返回分割结果的数组
    split_array = get_target_array1(value)
    name1 = split_array[0]  # 查询两个名字
    name2 = split_array[1]
    node1 = graph.run('MATCH(n{name:"' + name1 + '"}) return n').data()
    node2 = graph.run('MATCH(n{name:"' + name2 + '"}) return n').data()
    print(split_array)

    # 两个节点都存在
    if len(node1) and len(node2):
        # 如果该节点存在将该节点存入datas数组中
        # 构造字典存放节点信息
        dict_node1 = {
            'name': name1,
            'symbolSize': 50,
            'category': 'center'
        }
        datas.append(dict_node1)
        dict_node2 = {
            'name': name2,
            'symbolSize': 50,
            'category': 'center'
        }
        datas.append(dict_node2)
        # 查询该节点所涉及的所有 relationship，无向，步长为 1，并返回
        reps = graph.run('MATCH(n{name:"' + name1 + '"})<-[rel]->(m{name:"' + name2 + '"}) return rel').data()
        if len(reps):
            for r in reps:
                source = str(r['rel'].start_node['name'])
                target = str(r['rel'].end_node['name'])
                name = str(type(r['rel']).__name__)
                dict_node = {
                    'source': source,
                    'target': target,
                    'name': name
                }
                links.append(dict_node)
            # 构造字典存储 datas 和 links
            search_neo4j_data = {
                'data': datas,
                'links': links
            }
            # 转化为 json 格式
            search_neo4j_data = json.dumps(search_neo4j_data)
            return search_neo4j_data
        else:
            print("%s与%s之间没有直接关系。" % (name1, name2))
            return 0

    else:
        if len(node1) == 0 and len(node2) == 1:
            print("不存在人物%s！" % name1)
        if len(node1) == 1 and len(node2) == 0:
            print("不存在人物%s！" % name2)
        return 0


def question2(value):  # 根据节点和关系找人
    # 定义数据数组存储节点信息
    datas = []
    # 定义links数组存储关系信息
    links = []

    # 查询节点是否存在
    # 返回分割结果的数组
    split_array = get_target_array0(value)
    query_name = split_array[0]  # 查询名字
    query_relation = split_array[1]  # 查询关系
    query_node = graph.run('MATCH(n{name:"' + query_name + '"}) return n').data()
    print(split_array)

    # 如果节点存在 len(node) 的值为 1，不存在的话 len(node) 的值为 0
    if len(query_node):
        # 如果该节点存在将该节点存入datas数组中
        # 构造字典存放节点信息
        dict_node = {
            'name': query_name,
            'symbolSize': 50,
            'category': 'center'
        }
        datas.append(dict_node)

        # 查询与该节点具有该关系的节点，无向，步长为1，并返回这些节点
        # distinct!!! 数据集有些问题，需要distinct去重！
        nodes = graph.run("MATCH (n)-[r:%s]->(m) WHERE n.name = '%s' RETURN m" % (query_relation, query_name)).data()
        # 处理节点信息
        if len(nodes):
            for n in nodes:
                # 将节点信息的格式转化为 json
                node = json.dumps(n, ensure_ascii=False)
                node = json.loads(node)
                # 取出节点信息中的 name,label
                name = str(node['m']['name'])
                label = str(node['m']['label'])
                # 构造字典存放单个节点信息
                dict_node = {
                    'name': name,
                    'symbolSize': 50,
                    'category': label
                }
                # 将单个节点信息存储进data数组中
                datas.append(dict_node)

            # 查询该节点所涉及的所有 relationship，无向，步长为 1，并返回
            reps = graph.run('MATCH(n{name:"' + query_name + '"})-[rel:%s]->(m) return rel' % query_relation).data()
            for r in reps:
                source = str(r['rel'].start_node['name'])
                target = str(r['rel'].end_node['name'])
                name = str(type(r['rel']).__name__)
                dict_node = {
                    'source': source,
                    'target': target,
                    'name': name
                }
                links.append(dict_node)
            # 构造字典存储 datas 和 links
            search_neo4j_data = {
                'data': datas,
                'links': links
            }
            # 转化为 json 格式
            search_neo4j_data = json.dumps(search_neo4j_data)
            return search_neo4j_data

        else:
            print("%s没有%s" % (query_name, query_relation))
            return 0

    else:
        print("查无此节点")
        return 0


def search_all_rel():
    links = []  # 定义关系数组，存放节点间的关系
    # 查询所有关系，并将所有的关系信息存放在 links 数组中
    rps = graph.relationships
    for r in rps:
        source = str(rps[r].start_node['name'])  # 取出开始节点的name
        target = str(rps[r].end_node['name'])
        name = str(type(rps[r]).__name__)  # 取出开始节点的结束节点之间的关系
        # 构造字典存储单个关系信息
        dict_link = {
            'source': source,
            'target': target,
            'name': name
        }
        links.append(dict_link)  # 将单个关系信息存放进 links 数组中
    neo4j_data = {
        'links': links
    }
    neo4j_data = json.dumps(neo4j_data)
    return neo4j_data


def question4(value):  # 两个节点间的交集
    # 定义数据数组存储节点信息
    datas = []
    # 定义links数组存储关系信息
    links = []
    # 查询节点是否存在
    # 返回分割结果的数组
    split_array = get_target_array1(value)
    name1 = split_array[0]  # 查询两个名字
    name2 = split_array[1]
    node1 = graph.run('MATCH(n{name:"' + name1 + '"}) return n').data()
    node2 = graph.run('MATCH(n{name:"' + name2 + '"}) return n').data()
    print(split_array)
    # 两个节点都存在
    if len(node1) and len(node2):
        # 如果该节点存在将该节点存入datas数组中
        # 构造字典存放节点信息
        dict_node1 = {
            'name': name1,
            'symbolSize': 50,
            'category': 'center'
        }
        datas.append(dict_node1)
        dict_node2 = {
            'name': name2,
            'symbolSize': 50,
            'category': 'center'
        }
        datas.append(dict_node2)
        # 查询两个节点中间的交集节点，存入nodes中
        nodes = graph.run("MATCH (n{name:'%s'})--(b)--(m{name:'%s'}) where b.name<>n.name and \
                b.name<>m.name return distinct b " % (name1, name2)).data()
        if len(nodes):
            for n in nodes:
                # 将节点信息的格式转化为 json
                node = json.dumps(n, ensure_ascii=False)
                node = json.loads(node)
                # 取出节点信息中的 name,label
                name = str(node['b']['name'])
                label = str(node['b']['label'])
                # 构造字典存放单个节点信息
                dict_node = {
                    'name': name,
                    'symbolSize': 50,
                    'category': label
                }
                # 将单个节点信息存储进data数组中
                datas.append(dict_node)
                # 处理关系
                temp_relation = graph.run("MATCH (n{name:'%s'})-[r]-(b{name:'%s'}) RETURN r" % (name1, name))
                for r in temp_relation:
                    source = str(r['r'].start_node['name'])
                    target = str(r['r'].end_node['name'])
                    name_rel = str(type(r['r']).__name__)
                    dict_node = {
                        'source': source,
                        'target': target,
                        'name': name_rel
                    }
                    links.append(dict_node)
                # 另一边关系
                temp_relation = graph.run("MATCH (m{name:'%s'})-[s]-(b{name:'%s'}) RETURN s" % (name2, name))
                for r in temp_relation:
                    source = str(r['s'].start_node['name'])
                    target = str(r['s'].end_node['name'])
                    name_rel = str(type(r['s']).__name__)
                    dict_node = {
                        'source': source,
                        'target': target,
                        'name': name_rel
                    }
                    links.append(dict_node)
            # 构造字典存储 datas 和 links
            search_neo4j_data = {
                'data': datas,
                'links': links
            }
            # 转化为 json 格式
            search_neo4j_data = json.dumps(search_neo4j_data)
            return search_neo4j_data
        else:
            print("%s与%s之间没有交集" % (name1, name2))
            return 0
    else:
        if len(node1) == 0 and len(node2) == 1:
            print("不存在人物%s！" % name1)
        if len(node1) == 1 and len(node2) == 0:
            print("不存在人物%s！" % name2)

        return 0


def question5(value):
    """
    哪些人属于哪个nh？
    eg:哪些人物属于格兰杰家族
    """
    # 定义数据数组存储节点信息
    datas = []
    # 定义links数组存储关系信息
    links = []
    # 返回分割结果的数组
    split_array = get_target_array4(value)
    print(split_array)

    organization = split_array[0]
    node = graph.run(
        "MATCH (b) WHERE b.name CONTAINS '%s' AND b.label = '组织' RETURN b" % organization
    ).data()
    node_name = node[0]['b'].get('name')

    if len(node):
        # 如果该节点存在将该节点存入datas数组中
        # 构造字典存放节点信息
        dict_node = {
            'name': node_name,
            'symbolSize': 50,
            'category': 'center'
        }
        datas.append(dict_node)
        nodes = graph.run(
            "MATCH (m)-[r]->(b) WHERE b.name = '%s' RETURN m" % node_name
        ).data()

        # 处理节点信息
        for n in nodes:
            # 将节点信息的格式转化为 json
            node = json.dumps(n, ensure_ascii=False)
            node = json.loads(node)
            # 取出节点信息中的 name,label
            name = str(node['m']['name'])
            label = str(node['m']['label'])
            # 构造字典存放单个节点信息
            dict_node = {
                'name': name,
                'symbolSize': 50,
                'category': label
            }
            # 将单个节点信息存储进data数组中
            datas.append(dict_node)
        # 查询该节点所涉及的所有 relationship，无向，步长为 1，并返回
        reps = graph.run("MATCH (a)-[rel]->(b) WHERE b.name = '%s' RETURN rel" % node_name).data()
        for r in reps:
            source = str(r['rel'].start_node['name'])
            target = str(r['rel'].end_node['name'])
            name = str(type(r['rel']).__name__)
            dict_node = {
                'source': source,
                'target': target,
                'name': name
            }
            links.append(dict_node)
        # 构造字典存储 datas 和 links
        search_neo4j_data = {
            'data': datas,
            'links': links
        }
        # 转化为 json 格式
        search_neo4j_data = json.dumps(search_neo4j_data)
        return search_neo4j_data
    else:
        print("查无此节点")
        return 0


def question6(value):
    # 查找所有具有某关系的实体对
    # 定义数据数组存储节点信息
    datas = []
    # 定义links数组存储关系信息
    links = []
    # 查询关系是否存在
    target_relation = get_target_array6(value)
    relations = graph.run("MATCH(m) <- [r:%s]->(n) RETURN r" % target_relation)

    if relations is not None:
        # 先将涉及的所有节点找出并放入names中
        names = []
        for r in relations:
            source = str(r['r'].start_node['name'])
            target = str(r['r'].end_node['name'])
            names.append(source)
            names.append(target)
        # 去重
        names = list(set(names))

        for node_name in names:
            # 构造字典存放节点信息
            dict_node = {
                'name': node_name,
                'symbolSize': 50,
                'category': 'center'
            }
            datas.append(dict_node)
            # 为节点添加特定relation信息
            reps = graph.run('MATCH(n{name:"' + node_name + '"})<-[rel:%s]->(m) return rel'
                             % target_relation).data()
            for r in reps:
                source = str(r['rel'].start_node['name'])
                target = str(r['rel'].end_node['name'])
                name = str(type(r['rel']).__name__)
                dict_node = {
                    'source': source,
                    'target': target,
                    'name': name
                }
                links.append(dict_node)

        # 构造字典存储 datas 和 links
        search_neo4j_data = {
            'data': datas,
            'links': links
        }
        # 转化为 json 格式
        search_neo4j_data = json.dumps(search_neo4j_data)
        return search_neo4j_data
    else:
        print("图谱中未定义这种关系")
        return 0


def question7(value):
    # 凤凰社中哈利·波特的师生;凤凰社中哈利·波特的嫂子;邓布利多军中哈利·波特的同门
    # 复杂查询：某个组织里和 xx 有关系的人
    # 定义数据数组存储节点信息
    datas = []
    # 定义links数组存储关系信息
    links = []
    # 解析各个名称
    query_array = get_target_array7(value)
    print(query_array)
    query_org = query_array[0]
    query_name = query_array[1]
    query_rel = query_array[2]

    dict_node = {
        'name': query_name,
        'symbolSize': 50,
        'category': 'center'
    }
    datas.append(dict_node)
    dict_node = {
        'name': query_org,
        'symbolSize': 50,
        'category': '组织'
    }
    datas.append(dict_node)

    names = graph.run("MATCH (m:Organization {name:'%s'})-[:从属]-\
        (s:entity)-[:%s]-(n:entity{name:'%s'})RETURN DISTINCT s" % (query_org, query_rel, query_name)).data()

    if len(names):  # 遍历names
        for n in names:
            # 将节点信息的格式转化为 json
            node = json.dumps(n, ensure_ascii=False)
            node = json.loads(node)
            # 取出节点信息中的 name,label
            name_temp = str(node['s']['name'])
            label = str(node['s']['label'])
            # 构造字典存放节点信息
            dict_node = {
                'name': name_temp,
                'symbolSize': 50,
                'category': label
            }
            datas.append(dict_node)

            # 为节点添加与查询人物的特定关系
            reps = graph.run('MATCH(n{name:"' + name_temp + '"})<-[rel]->(m{name:"' + query_name + '"})'
                                                                                                   ' return rel').data()
            for r in reps:
                source = str(r['rel'].start_node['name'])
                target = str(r['rel'].end_node['name'])
                name = str(type(r['rel']).__name__)
                dict_node = {
                    'source': source,
                    'target': target,
                    'name': name
                }
                links.append(dict_node)

            # 添加与组织的关系
            reps = graph.run(
                'MATCH(n{name:"' + name_temp + '"})<-[rel]->(m{name:"' + query_org + '"}) return rel').data()
            for r in reps:
                source = str(r['rel'].start_node['name'])
                target = str(r['rel'].end_node['name'])
                name = str(type(r['rel']).__name__)
                dict_node = {
                    'source': source,
                    'target': target,
                    'name': name
                }
                links.append(dict_node)

        # 构造字典存储 datas 和 links
        search_neo4j_data = {
            'data': datas,
            'links': links
        }
        # 转化为 json 格式
        search_neo4j_data = json.dumps(search_neo4j_data)
        return search_neo4j_data
    else:
        print("不存在这样的节点")
        return 0


def getfunc(value):
    choose = classify(value)
    if choose == 1:
        return question1(value)
    elif choose == 2:
        return question2(value)
    elif choose == 3:
        return question3(value)
    elif choose == 4:
        return question4(value)
    elif choose == 5:
        return question5(value)
    elif choose == 6:
        return question6(value)
    elif choose == 7:
        return question7(value)
    else:
        return 0


def get_tag(value):
    if value == 'no_name' or value not in taged_names:  # 没有 tag
        print("无tag")
        return "小组成员：曹嘉悦、邓薇薇、林帆、唐明昊"
    if value in main_role:
        return 'main_role'
    # 查询节点是否存在
    node = graph.run('MATCH(n{name:"' + value + '"}) return n').data()
    # 如果节点存在 len(node) 的值为 1，不存在的话 len(node) 的值为 0
    temp = json.dumps(node, ensure_ascii=False)
    temp = json.loads(temp)
    # 取出节点信息
    tag = str(temp[0]['n']['tag'])
    return tag
