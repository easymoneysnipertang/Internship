from config import *
graph.delete_all()  # 删除已有数据库内容

# 导入neo4j数据库
name_set = set()  # 用来去重
with open("./relations_final.csv", encoding='utf-8') as f:
    for line in f.readlines():
        rela_array = line.strip("\n").split(",")
        print(rela_array)
        # 调整三元组
        rela_array = [rela_array[0], rela_array[-1], rela_array[1]]
        # 创建节点
        # 去重，名字不要重复
        if rela_array[0] not in name_set:
            graph.run("MERGE(p: entity{name: '%s', label:'对象'})" % (rela_array[0]))
            name_set.add(rela_array[0])
        if rela_array[2] not in name_set:
            # 区分实体标签
            if rela_array[1] == "职业":
                graph.run("MERGE(p: Occupation{name: '%s', label:'职业'})" % (rela_array[2]))
            elif rela_array[1] == "从属":
                graph.run("MERGE(p: Organization{name: '%s', label:'组织'})" % (rela_array[2]))
            else:
                graph.run("MERGE(p: entity{name: '%s', label:'对象'})" % (rela_array[2]))
            name_set.add(rela_array[2])
        # 建立关系
        graph.run(
            "MATCH(e), (cc) \
            WHERE e.name='%s' AND cc.name='%s'\
            CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
            RETURN r" % (rela_array[0], rela_array[2], rela_array[1], rela_array[1])
        )
f.close()
