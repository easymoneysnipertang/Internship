import operator
import networkx as nx
from py2neo import *
import json

# 连接数据库
graph = Graph('bolt: // localhost:7687', auth=('neo4j', '12345678'))
rel_list = []


def get_rel_list():
    reps = graph.run('MATCH(n)<-[rel]->(m) return rel limit 2000').data()  # 一共有 3476 条，取 2000 够了
    for r in reps:
        source = str(r['rel'].start_node['name'])
        target = str(r['rel'].end_node['name'])
        rel = "%s  %s" % (source, target)
        rel_list.append(rel)


def get_page_rank():
    # Pagerank 可以估算任何网络中节点的重要性
    fb = nx.parse_edgelist(rel_list, nodetype=str)
    page_ranks = nx.pagerank(fb)
    sorted_pagerank = sorted(page_ranks.items(), key=operator.itemgetter(1), reverse=True)
    sorted_pagerank = dict(sorted_pagerank[:300])  # 截取前300个
    return sorted_pagerank


def get_centrality():
    # 介数中心性衡量了特定节点出现在两个其他节点之间最短路径集的次数
    fb = nx.parse_edgelist(rel_list, nodetype=str)
    betweenness_centrality = nx.betweenness_centrality(fb, normalized=True, endpoints=True)
    return list(betweenness_centrality.keys())[:300]  # 截取前300个


def get_nodes_from_neo4j(value):
    # 根据名字从 neo4j 找出相关节点
    datas = []
    # 查询节点是否存在
    node = graph.run('MATCH(n{name:"' + value + '"}) return n').data()
    # 如果节点存在 len(node) 的值为 1，不存在的话 len(node) 的值为 0
    if len(node):
        # 查询相关节点
        nodes = graph.run('MATCH(n{name:"' + value + '"})<-->(m) return distinct m').data()
        # 相邻节点全部存起来
        for n in nodes:
            # 将节点信息的格式转化为 json
            node = json.dumps(n, ensure_ascii=False)
            node = json.loads(node)
            # 取出节点信息中的 name,label
            name = str(node['m']['name'])
            datas.append(name)
    return datas


def get_related_nodes(value, rank_list, center_list):  # 根据一个名字推荐三个相关节点
    datas = get_nodes_from_neo4j(value)
    related_nodes = []
    if len(datas):
        # 找两个相邻节点且 pagerank 最高的
        count = 0
        for key in rank_list:
            if key in datas:
                related_nodes.append(key)
                count += 1
                if count == 3:
                    break
        for key in center_list:
            if (key in datas) and (key not in related_nodes):
                related_nodes.append(key)
                count += 1
                if count == 4:
                    break
    else:
        related_nodes = ''
    return related_nodes
