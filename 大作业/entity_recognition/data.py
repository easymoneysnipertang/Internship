from os.path import join
from codecs import open
import re
import random

"""
build_corpus方法
构建语料库，读取数据并生成用于训练和评估的句子列表和标签列表
"""
def build_corpus(split, add_words_list, add_tag_list, make_vocab=True, data_dir="./ResumeNER"):
    """读取数据"""
    assert split in ['train', 'dev', 'test']

    word_lists = []
    tag_lists = []
    with open(join(data_dir, split+".char.bmes"), 'r', encoding='utf-8') as f:
        word_list = []
        tag_list = []
        # 逐行处理，将内容拆分为单词和对应标签
        for line in f:
            if line != '\n':
                word, tag = line.strip('\n').split()
                word_list.append(word)
                tag_list.append(tag)
            else:
                word_lists.append(word_list)
                tag_lists.append(tag_list)
                word_list = []
                tag_list = []

    # 根据数据集的划分类型将额外提供的数据合并到相应的训练集、验证集或测试集中，以扩充原始数据集的规模
    if split == 'train':
        word_lists = word_lists + add_words_list[: int(0.8 * len(add_words_list))]
        tag_lists = tag_lists + add_tag_list[: int(0.8 * len(add_tag_list))]
    elif split == 'dev':
        word_lists = word_lists + add_words_list[int(0.8 * len(add_words_list)): int(0.9 * len(add_words_list))]
        tag_lists = tag_lists + add_tag_list[int(0.8 * len(add_tag_list)): int(0.9 * len(add_words_list))]
    else:
        word_lists = word_lists + add_words_list[int(0.9 * len(add_words_list)): ]
        tag_lists = tag_lists + add_tag_list[int(0.9 * len(add_tag_list)): ]

    # 如果make_vocab为True，还需要返回word2id和tag2id
    # 训练阶段需要构建词汇表，以将单词和标签映射为唯一的整数索引
    # 而在验证集和测试集阶段不需要构建词汇表，只需要使用训练阶段构建的词汇表进行索引映射即可
    if make_vocab:
        word2id = build_map(word_lists)
        tag2id = build_map(tag_lists)
        return word_lists, tag_lists, word2id, tag2id
    else:
        return word_lists, tag_lists

def build_corpus_origin(split, make_vocab=True, data_dir="./ResumeNER"):
    """读取数据，与build_corpus方法的区别是没有数据扩充"""
    assert split in ['train', 'dev', 'test']

    word_lists = []
    tag_lists = []
    with open(join(data_dir, split+".char.bmes"), 'r', encoding='utf-8') as f:
        word_list = []
        tag_list = []
        for line in f:
            if line != '\n':
                word, tag = line.strip('\n').split()
                word_list.append(word)
                tag_list.append(tag)
            else:
                word_lists.append(word_list)
                tag_lists.append(tag_list)
                word_list = []
                tag_list = []

    # 如果make_vocab为True，还需要返回word2id和tag2id
    if make_vocab:
        word2id = build_map(word_lists)
        tag2id = build_map(tag_lists)
        return word_lists, tag_lists, word2id, tag2id
    else:
        return word_lists, tag_lists

"""
build_map方法
构建映射
"""
def build_map(lists):
    maps = {}
    for list_ in lists:
        for e in list_:
            if e not in maps:
                maps[e] = len(maps)

    return maps

"""
process_BosonNLP_data方法
处理BosonNLP数据集，将原始文本数据转换为适合进行序列标注的格式
"""
def process_BosonNLP_data(data_dir="./ResumeNER"):
    with open(data_dir + "/BosonNLP_NER_6C.txt", "r", encoding="utf-8") as f:
        total_lines = [line.strip() for line in f.readlines()]

    total_lines = [line for line in total_lines if line != ''] # 去除空行
    cutLineFlag = ["！", "。", "!"] # 分隔符
    sentenceList = []
    # 遍历每一行的每个字符，根据切割符号将字符组合成完整的句子，并将满足长度要求的句子添加到sentenceList列表中
    for words in total_lines:
        oneSentence = ""
        for word in words:
            if word not in cutLineFlag:
                oneSentence = oneSentence + word
            else:
                oneSentence = oneSentence + word
                if oneSentence.__len__() > 4:
                    sentenceList.append(oneSentence.strip())
                oneSentence = ""

    return transfer_str2label(sentenceList)

"""
seperate_ch方法
将序列分隔为单个字符
"""
def seperate_ch(sequence):
    return [ch for ch in sequence]

"""
decode方法
将特定格式的字符串seq解码为对应的序列和标签
BMEO格式
"""
def decode(seq):
    # new_seq = ""
    # new_tag = ""
    if "time" in seq:
        new_seq = seq[7:-2]
        new_tag = ["O"] * len(new_seq)
    elif "location" in seq:
        new_seq = seq[11:-2]
        if len(new_seq) == 2:
            new_tag = ["B-LOC", "E-LOC"]
        else:
            new_tag = ["B-LOC"] + ["M-LOC"] * (len(new_seq)-2) + ["E-LOC"]
    elif "person_name" in seq:
        new_seq = seq[14:-2]
        if len(new_seq) == 1:
            new_tag = ["S-NAME"]
        elif len(new_seq) == 2:
            new_tag = ["B-NAME", "E-NAME"]
        else:
            new_tag = ["B-NAME"] + ["M-NAME"] * (len(new_seq)-2) + ["E-NAME"]
    elif "org_name" in seq:
        new_seq = seq[11:-2]
        if len(new_seq) == 1:
            new_tag = ["S-ORG"]
        elif len(new_seq) == 2:
            new_tag = ["B-ORG", "E-ORG"]
        else:
            new_tag = ["B-ORG"] + ["M-ORG"] * (len(new_seq)-2) + ["E-ORG"]
    elif "company_name" in seq:
        new_seq = seq[15:-2]
        if len(new_seq) == 1:
            new_tag = ["S-COM"]
        elif len(new_seq) == 2:
            new_tag = ["B-COM", "E-COM"]
        else:
            new_tag = ["B-COM"] + ["M-COM"] * (len(new_seq)-2) + ["E-COM"]
    elif "product_name" in seq:
        new_seq = seq[15:-2]
        if len(new_seq) == 1:
            new_tag = ["S-PROD"]
        elif len(new_seq) == 2:
            new_tag = ["B-PROD", "E-PROD"]
        else:
            new_tag = ["B-PROD"] + ["M-PROD"] * (len(new_seq)-2) + ["E-PROD"]
    
    return new_seq, new_tag


"""
transfer_str2label方法
将输入的sentenceList列表转换为模型训练所需的句子列表和标签列表
"""
def transfer_str2label(sentenceList):
    sent_list = []
    tag_list = []
    for sent in sentenceList:
        if "{{" in sent and len(sent) > 4:
            # 使用正则表达式找到“{{”和“}}”的位置
            start = [item.start() for item in re.finditer("{{", sent)]
            end = [item.end() for item in re.finditer("}}", sent)]
            # 如果数量不一致说明标记有误，跳过这个句子
            if len(start) != len(end):
                continue

            left = 0  # left用于记录上一个“”}}“”的位置
            new_str = ""
            new_tag = []
            for i in range(len(start)):
                # left到start[i]之间的部分存入new_str，是"{{"之前的普通文本
                new_str = new_str + sent[left: start[i]]
                # 新增O标签
                new_tag = new_tag + ['O'] * (start[i]-left)
                # 解码""{{""和""}}""之间
                sub_str, sub_tag = decode(sent[start[i]: end[i]])
                new_str = new_str + sub_str
                new_tag = new_tag + sub_tag
                left = end[i]

            # 将剩余文本做同样处理
            new_str = new_str + sent[left: len(sent)]
            new_tag = new_tag + ['O'] * (len(sent)-left)
        
        if len(new_str) == len(new_tag):
            sent_list.append(seperate_ch(new_str))
            tag_list.append(new_tag)

    # 进行顺序打乱然后返回
    shuffle_index = list(range(len(sent_list)))
    random.shuffle(shuffle_index)
    return [sent_list[i] for i in shuffle_index], [tag_list[i] for i in shuffle_index]

