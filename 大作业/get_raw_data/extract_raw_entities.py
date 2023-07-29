import requests
from lxml import etree
from bs4 import BeautifulSoup

import random
import time
import os

seeds = ['Category:霍格沃茨职工',
         'Category:霍格沃茨学生',
         'Category:第一次凤凰社',
         'Category:魔法部雇员',
         'Category:食死徒',
         'Category:麻瓜']

root = 'https://harrypotter.fandom.com/zh/wiki/'

user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
# 完成随机选取 user-agent，实现 反 反爬 操作
request_headers = {
    'user-agent': random.choice(user_agents),
    'Referer': 'https://harrypotter.fandom.com/'
}

all_entities = []
current_category = [x for x in seeds]  #储存还需要处理的类别链接，初始是设置的种子
have_seen_categories = set([x for x in seeds])  #储存已处理过的类别链接

while len(current_category) >= 1:
    seed = current_category.pop(0)
    print('visiting', seed)
    url = root + seed
    resp = requests.get(url=url, headers=request_headers)
    html_text = resp.text
    # 解析为 soup 文档
    soup = BeautifulSoup(html_text, "lxml")
    selector = etree.HTML(html_text)
    a_list = soup.select('a.category-page__member-link')
    cur_ents = []
    for a in a_list:
        cur_ents.append(a['title'])

    for t in cur_ents:
        if 'Template' in t:
            continue
        if 'Category' in t:
            if t not in have_seen_categories:
                current_category.append(t)
                have_seen_categories.add(t)
        else:
            all_entities.append(t)
    time.sleep(1)

# 转化为集合为了去重，再转化回list,最后sorted排序
all_entities = sorted(list(set(all_entities)))

filename = './data/entities.txt'
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, 'w', encoding='utf-8') as f:
    for t in all_entities:
        f.write(t.strip() + '\n')


