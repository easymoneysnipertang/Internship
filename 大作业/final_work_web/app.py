from flask import Flask, render_template, request
from graph_select import *
from recommend import get_rel_list, get_page_rank, get_centrality, get_related_nodes

app = Flask(__name__, static_folder='static')
get_rel_list()  # 填充关系表
page_rank = get_page_rank()  # 得到 page_rank
centrality = get_centrality()  # 得到 centrality


@app.route('/')
def hello_harry():  # 进入主页
    return render_template('home.html')


@app.route('/graph')
def graph_harry():  # 进入图谱查询页面,重点在于进入一个新的初始好的index.html
    return render_template('graph.html')


@app.route('/graph/Gryffondor_search')
def gryffondor_graph():
    ctx = {}
    node_name = "格兰芬多学院"
    # 查询结果
    search_neo4j_data = question1(node_name)
    # 给出对应的tag
    tag = get_tag(node_name)
    # 给出推荐的节点
    high_nodes = get_related_nodes(node_name, page_rank, centrality)  # 从page_rank和 centrality 里挑三个推荐节点
    print(high_nodes)
    str2return = ''  # 合成为一个字符串
    for s in high_nodes:
        str2return += s + "|"
    related_node = str2return
    print(str2return)
    return render_template('graph.html', ctx=ctx, search_neo4j_data=search_neo4j_data, node_name=node_name,
                           related_node=related_node, tag=tag)


@app.route('/graph/Slytherin_search')
def slytherin_graph():
    ctx = {}
    node_name = "斯莱特林学院"
    # 查询结果
    search_neo4j_data = question1(node_name)
    # 给出对应的tag
    tag = get_tag(node_name)
    # 给出推荐的节点
    high_nodes = get_related_nodes(node_name, page_rank, centrality)  # 从page_rank和 centrality 里挑三个推荐节点
    print(high_nodes)
    str2return = ''  # 合成为一个字符串
    for s in high_nodes:
        str2return += s + "|"
    related_node = str2return
    print(str2return)
    return render_template('graph.html', ctx=ctx, search_neo4j_data=search_neo4j_data, node_name=node_name,
                           related_node=related_node, tag=tag)


@app.route('/graph/Ravenclaw_search')
def ravenclaw_graph():
    ctx = {}
    node_name = "拉文克劳学院"
    # 查询结果
    search_neo4j_data = question1(node_name)
    # 给出对应的tag
    tag = get_tag(node_name)
    # 给出推荐的节点
    high_nodes = get_related_nodes(node_name, page_rank, centrality)  # 从page_rank和 centrality 里挑三个推荐节点
    print(high_nodes)
    str2return = ''  # 合成为一个字符串
    for s in high_nodes:
        str2return += s + "|"
    related_node = str2return
    print(str2return)
    return render_template('graph.html', ctx=ctx, search_neo4j_data=search_neo4j_data, node_name=node_name,
                           related_node=related_node, tag=tag)


@app.route('/graph/Hufflepuff_search')
def hufflepuff_graph():
    ctx = {}
    node_name = "赫奇帕奇学院"
    # 查询结果
    search_neo4j_data = question1(node_name)
    # 给出对应的tag
    tag = get_tag(node_name)
    # 给出推荐的节点
    high_nodes = get_related_nodes(node_name, page_rank, centrality)  # 从page_rank和 centrality 里挑三个推荐节点
    print(high_nodes)
    str2return = ''  # 合成为一个字符串
    for s in high_nodes:
        str2return += s + "|"
    related_node = str2return
    print(str2return)
    return render_template('graph.html', ctx=ctx, search_neo4j_data=search_neo4j_data, node_name=node_name,
                           related_node=related_node, tag=tag)


@app.route('/graph/select', methods=['POST'])
def graph_selection():  # 进入页面后进行查询
    ctx = {}
    # 接收前端传过来的查询值
    str_value = request.form.get('node')
    print(str_value)
    # 查询结果
    search_neo4j_data = getfunc(str_value)
    # 未查询到该节点
    if search_neo4j_data == 0:
        ctx = {'title': '数据库中暂未添加该实体'}
        return render_template('graph.html', ctx=ctx)
    # 查询到了该节点
    else:
        node_name = get_name(str_value)  # 截取一个名字
        print(node_name)
        # 给出相关文本
        tag = get_tag(node_name)
        # 给出推荐的节点
        high_nodes = get_related_nodes(node_name, page_rank, centrality)  # 从page_rank和 centrality 里挑三个推荐节点
        if node_name == 'no_name':  # 若给出的名字无 tag
            node_name = str_value
        str2return = ''  # 合成为一个字符串
        for s in high_nodes:
            str2return += s + "|"
        related_node = str2return
        return render_template('graph.html', ctx=ctx, search_neo4j_data=search_neo4j_data,
                               node_name=node_name, related_node=related_node, tag=tag)


if __name__ == '__main__':
    app.run()
