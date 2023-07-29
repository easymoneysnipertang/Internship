# 介绍
本工程旨在使用基于HMM，CRF，Bi-LSTM，Bi-LSTM+CRF搭建中文命名实体识别模型。

# 文件目录说明
ResumeNER/        存放数据集
models/           存放模型相关文件
ckpt/             存放训练好的模型参数
data.py           数据集预处里相关函数
utils.py          生成字典，保存、加载模型等相关函数
evaluating.py     评价模型的指标函数
evaluate.py       评估模型函数
train_model.py    模型训练
test_model.ipynb  模型测试

# 数据集
我们共使用了两个数据集来训练实体模型。
1. 论文ACL 2018[Chinese NER using Lattice LSTM](https://github.com/jiesutd/LatticeLSTM)中收集的简历数据。数据的格式如下，它的每一行由一个字及其对应的标注组成，标注集采用BIOES，句子之间用一个空行隔开。
    美	B-LOC
    国	E-LOC
    的	O
    华	B-PER
    莱	I-PER
    士	E-PER

    我	O
    跟	O
    他	O
    谈	O
    笑	O
    风	O
    生	O

2. BosonNLP_NER，波森命名实体语料，由一段句子与其对应标注组成，选取其中一句预料如下。
{{product_name:浙江在线杭州}}{{time:4月25日}}讯（记者{{person_name: 施宇翔}} 通讯员 {{person_name:方英}}）毒贩很“时髦”，用{{product_name:微信}}交易毒品。没料想警方也很“潮”，将计就计，一举将其擒获。
在训练前，会将BosonNLP_NER数据集处理成与前一个数据集相同的形式，并一同去训练我们的命名实体识别模型。

# 模型训练
运行train_model.py搭建中文命名实体识别模型
