import re
import os

def clean_r(s):
    # 将一些特殊字符替换
    s = re.sub(r'\(', '', s)
    s = re.sub(r'\)', '', s)
    s = re.sub(r'\[', '', s)
    s = re.sub(r'\]', '', s)
    s = re.sub(r'\d+', '', s)
    s = re.sub(r'†', '', s)
    # 拆分
    if '/' in s:
        s = s.split('/')[0]
    if '，' in s:
        s = s.split('，')[0]
    return s

def clean_e(s):
    # 去掉括号即之间的
    s = re.sub(r'\([^)]*\)', '', s)
    s = re.sub(r'\（[^)]*\）', '', s)
    return s


def read_relations(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.readlines()
    relations = []
    for row in data:
        d = row.strip().split()
        relations.append(d)
    return relations


relations = read_relations('./data1/extent_relations.txt')
#relations = read_relations('./data/relations.txt')
clean_relations = []
for d in relations:  # 遍历得到的每一行关系
    if len(d) != 3: continue  # 大于三个舍去
    if d[-1][0] == '(' and d[-1][-1] == ')': continue # 第三个元素(即第二个实体)是括号包括的形式舍去
    if d[-1] == '-': continue # 第三个元素(即第二个实体)是-舍去
    d[1] = clean_r(d[1]) # 对第二个元素(即关系)进行clean
    if d[1] == '可能': continue # 对第二个元素(即关系)是可能则删去
    d[2] = clean_e(d[2])
    if '(' in d[2] and ')' not in d[2]: continue
    if '(' not in d[2] and ')' in d[2]: continue
    if '（' in d[2] and '）' not in d[2]: continue
    if '(' not in d[2] and '）' in d[2]: continue
    clean_relations.append(d)

filename = './data1/extent_relations_clean.txt'
#filename = './data/relations_clean.txt'
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, 'w', encoding='utf-8') as f:
    for r in clean_relations:
        f.write('%s\t%s\t%s\n' % (r[0], r[1], r[2]))

