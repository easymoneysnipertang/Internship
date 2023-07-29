raw_relations = './data1/relations.txt'
extracted_relations = '../relation_extraction/data/relation_clean.csv'
relations_final = './data1/relations_final.csv'

data = []
with open(raw_relations, 'r', encoding='utf-8') as f:
    for x in f.readlines():
        d = x.strip().split()
        if(d[1]=='相关家族'):
            continue
        else:
            data.append([d[0], d[-1], d[1]])

def replace_dot(s):
    return s.replace('.', '·')

def remove_repeated(data):
    res = set()
    for d in data:
        res.add((d[0],d[1],d[2]))
    return sorted(list(res))


with open(extracted_relations, 'r', encoding='utf-8') as f:
    for x in f.readlines():
        d = x.strip().split(',')
        data.append([replace_dot(d[0]), replace_dot(d[1]), replace_dot(d[2])])


data = remove_repeated(data)
with open(relations_final, 'w', encoding='utf-8') as f:
    for d in data:
        f.write('%s,%s,%s\n'%(d[0],d[1],d[2]))

