from bs4 import BeautifulSoup
import requests
import re
import os
root = 'https://harrypotter.fandom.com/zh/wiki/'

"""
使用正则表达式删去方括号与其中的数字如[1]
"""
def clean_string(s):
    s = re.sub(r'\[\d*\]', '', s)
    return s

"""
extract_entity方法用于获取一个实体的关系
"""
def extract_entity(ent):
    url = root + ent
    response = requests.get(url=url).content
    soup = BeautifulSoup(response, 'html.parser')
    e1 = ent
    relations = []
    # 找到指定class的div标签
    for p in soup.find_all('div', attrs={'class': 'pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background'}):
        if p.text == '家庭信息':  # 判断得到的div标签是否包含‘家庭信息’
            for np in p.next_siblings:   # 遍历后续兄弟结点
                if np.find_all('div')[0].text == '家庭成员':
                    for relation in np.find_all('li'):
                        tmp = relation.text.split()
                        if len(tmp) >= 2:
                            # 根据网页中显示的信息，把第二个元素及其以后clean得到实体关系，第一个元素clean后得到实体
                            r = (clean_string(tmp[1][1:-1]), clean_string(tmp[0]))
                            relations.append(r)
        elif p.text == '关系信息': # 判断得到的div标签是否包含‘关系信息’
            for np in p.next_siblings:  # 遍历后续兄弟结点
                r = clean_string(np.find_all('div')[0].text)
                for e2 in np.find_all('li'):
                    e = clean_string(e2.text)
                    if len(e.split()) > 1:
                        for ee in e.split():
                            relations.append((r, ee))
                    else:
                        relations.append((r, e))
    relations = [(e1, r[0], r[1]) for r in relations]
    return relations


# 集合，存不重复的关系
all_relations = set()

"""
为了获取更多的实体和关系
"""
with open('./data1/extent_entities.txt', 'r', encoding='utf-8') as f:
#with open('./data/entities.txt', 'r', encoding='utf-8') as f:
    ents = [e.strip() for e in f.readlines()]
    for e in ents:
        print('processing', e)
        relations = extract_entity(e)
        for r in relations:
            all_relations.add(r)

all_relations = sorted(list(all_relations))

#filename = './data/relations.txt'
filename = './data1/extent_relations.txt'
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, 'w', encoding='utf-8') as f:
    for r in all_relations:
        f.write('%s\t%s\t%s\n' % (r[0], r[1], r[2]))

