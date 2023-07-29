# -*- coding: utf-8 -*-
import pyltp 
import os
from config import graph

LTP_DATA_DIR = 'kgqa\\ltp_data_v3.4.0'
# LTP_DATA_DIR = 'ltp_data_v3.4.0'
# 在neo4j中查询所有标签为“组织”的节点
medicine = ['活地狱汤剂', '欢欣剂', '打嗝药水', '永恒药剂']
friend_str = ['好友', '交集', '共友']


def cut_words(words):
    # segmentor = pyltp.Segmentor()
    # seg_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    # segmentor.load(seg_model_path)

    seg_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # ltp模型路径
    segmentor = pyltp.Segmentor(model_path=seg_model_path)  # 初始化并加载ltp模型，segmentor类用于中文分词

    words = segmentor.segment(words)  # 对传入参数words进行分词
    segmentor.release()  # 释放资源

    # print(words)
    # array_str="|".join(words)
    # array=array_str.split("|")
    # segmentor.release()  # 释放资源
    # return array

    return words


def words_mark(array):
    # 词性标注模型路径，模型名称为`pos.model`
    # pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    # postagger = pyltp.Postagger()  # 初始化实例
    # postagger.load(pos_model_path)  # 加载模型

    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    postagger = pyltp.Postagger(model_path=pos_model_path)  # 初始化实例

    postags = postagger.postag(array)  # 词性标注
    postagger.release()  # 释放模型

    # pos_str=' '.join(postags)
    # pos_array=pos_str.split(" ")
    # postagger.release()  # 释放模型

    return postags


def get_target_array0(words):
    target_pos = ['nh', 'n']  # 目标标注词性：名字+名词
    target_array = []  # 结果
    seg_array = cut_words(words)
    print("111")
    print(seg_array)
    pos_array = words_mark(seg_array)
    print(pos_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])
    # target_array.append(seg_array[1])
    return target_array


def get_target_array1(words):
    target_pos = ['nh', 'nh']  # 目标标注词性：名字+名词
    target_array = []  # 结果
    seg_array = cut_words(words)
    print("111")
    print(seg_array)
    pos_array = words_mark(seg_array)
    print(pos_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])
    # target_array.append(seg_array[1])
    return target_array


def get_target_array2(words):
    target_pos = ['nh', 'nh']  # 目标标注词性：名字+名词
    target_array = []  # 结果
    seg_array = cut_words(words)
    print("111")
    print(seg_array)
    pos_array = words_mark(seg_array)
    print(pos_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])
    # target_array.append(seg_array[1])
    return target_array


def get_target_array4(words):
    """
    哪些人属于哪个n？
    eg:哪些人物属于格兰杰家族
    """
    target_pos = ['nh']
    target_array = []
    seg_array = cut_words(words)
    print("111")
    print(seg_array)
    pos_array = words_mark(seg_array)
    print(pos_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])
        # target_array.append(seg_array[1])
    return target_array


def get_target_array6(words):
    seg_array = cut_words(words)
    for i in range(len(seg_array)):
        if i > 0 and seg_array[i] == '关系':
            return seg_array[i-1]


def get_target_array7(words):
    word_array = cut_words(words)
    ns = words_mark(word_array)

    org = ""
    for i in range(len(word_array)):
        if word_array[i] in Organization:
            org += word_array[i]
            ns[i] = 'wp'  # 当作标点，在后面查询人名时忽略
            break
        elif i+1 < len(word_array):
            temp = word_array[i]+word_array[i+1]
            if temp in Organization:
                org += temp
                ns[i] = ns[i+1] = 'wp'
                break
        elif i+2 < len(word_array):
            temp = word_array[i]+word_array[i+1]+word_array[i+2]
            if temp in Organization:
                org += temp
                ns[i] = ns[i+1] = ns[i+2] = 'wp'
                break
        elif i+3 < len(word_array):
            temp = word_array[i]+word_array[i+1]+word_array[i+2]+word_array[i+3]
            if temp in Organization:
                org += temp
                ns[i] = ns[i+1] = ns[i+2] = ns[i+3] = 'wp'
                break
        else:
            continue

    # 在删除组织后的数组中遍历寻找人名和关系
    res = []
    res.append(org)
    for i in range(len(ns)):
        if ns[i] == 'nh':
            res.append(word_array[i])
        elif ns[i] == 'n':
            res.append(word_array[i])
    return res  # org,name,rel


def classify(word):
    # 判断是否为药剂
    if word in medicine:
        return 1

    # 判断问句的查询类型：
    words = cut_words(word)
    ns = words_mark(words)
    # print(words,ns)

    # 判断人名个数
    count_nh = 0
    for i in range(len(ns)):
        if ns[i] == 'nh':
            count_nh += 1

    # 判断是否只输入了人名
    if len(words) == 1:
        if ns[0] == 'nh':
            return 1
        else:
            return 0  # 未知提问类型

    # 用词性数组判断是否为2类型
    if ns[0] == 'nh' and ns[2] == 'n':
        return 2

    # 字符串匹配
    org_flag = 0
    person_flag = 0
    # 遍历words，是否在查询“交集/共同好友“等明显特征
    for i in range(len(words)):
        str_word = words[i]
        #  print(str)
        if str_word in friend_str:
            return 4  # 看一下限定是两个
        elif str_word == "关系":
            if count_nh == 2:
                return 3
            elif count_nh == 0:
                return 6
        elif str_word == "人物":
            person_flag += 1
        elif str_word in Organization:
            org_flag += 1
        if i+1 < len(words):
            temp = str_word+words[i+1]
            #  print(temp)
            if temp in Organization:
                org_flag += 1
        if i+2 < len(words):
            temp = str_word + words[i + 1]+words[i+2]
            if temp in Organization:
                org_flag += 1
        if i+3 < len(words):
            temp = str_word + words[i + 1] + words[i + 2] + words[i+3]
            if temp in Organization:
                org_flag += 1

    # 区分5和7
    if person_flag > 0:
        return 5
    else:
        return 7


def find_org_list():
    # 找出所有属性为“组织”的节点
    data = graph.run("MATCH (n:Organization) RETURN n.name")
    data = list(data)
    # print('节点',data)
    res = []  # name保存到res
    for node in data:
        #  print(node[0])
        res.append(node[0])
    #  print(res)
    return res


Organization = find_org_list()


def get_name(value):
    if value in medicine:
        return value
    word_array = cut_words(value)
    ns = words_mark(word_array)
    for i in range(len(ns)):
        if ns[i] == 'nh':
            return word_array[i]
    return 'no_name'


if __name__ == '__main__':
    # test_words="哈利·波特的侄女是谁？"
    test_words = "哈利·波特和乔治·韦斯莱是什么关系？"
    test_array = cut_words(test_words)
    print(test_array)

    test_n = words_mark(test_array)
    print(test_n)

    test_target = get_target_array1(test_words)
    print(test_target)


#     test = [
#         '哈利·波特',  # 1
#         '活地狱汤剂',  # 1
#         '欢欣剂',  # 1
#         '打嗝药水',  # 1
#         '永恒药剂',  # 1
#         '哈利·波特的侄女是谁？',  # 2
#         '哈利·波特和乔治·韦斯莱是什么关系？',  # 3
#         '哈利·波特和乔治·韦斯莱的交集？',  # 4
#         '哈利·波特和乔治·韦斯莱的共同好友',  # 4
#         '哪些人物属于格兰杰家庭？',  # 5
#         '格兰杰家庭有哪些人物？',  # 5
#         '哪些人物属于斯莱特林家族？',  # 5
#         '查找具有父亲关系的所有人物对',  # 6
#         '查找凤凰社中哈利·波特的同门。',  # 7
#     ]
#     # 不支持“是....吗？”类型的问题
