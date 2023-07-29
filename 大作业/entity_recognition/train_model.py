from data import build_corpus, process_BosonNLP_data, build_corpus_origin
from utils import extend_maps, prepocess_data_for_lstmcrf
from evaluate import bilstm_train_and_eval

def main():
    """训练模型，评估结果"""

    # 读取数据
    print("读取数据...")
    boson_word_lists, boson_tag_lists = process_BosonNLP_data()
    train_word_lists, train_tag_lists, word2id, tag2id = build_corpus("train", boson_word_lists, boson_tag_lists)
    dev_word_lists, dev_tag_lists = build_corpus("dev", boson_word_lists, boson_tag_lists, make_vocab=False)
    test_word_lists, test_tag_lists = build_corpus("test", boson_word_lists, boson_tag_lists, make_vocab=False)

    # 训练评估BI-LSTM模型
    print("正在训练评估Bi-LSTM模型...")
    bilstm_word2id, bilstm_tag2id = extend_maps(word2id, tag2id, for_crf=False)
    lstm_pred = bilstm_train_and_eval(
        (train_word_lists, train_tag_lists),
        (dev_word_lists, dev_tag_lists),
        (test_word_lists, test_tag_lists),
        bilstm_word2id, bilstm_tag2id,
        crf=False
    )


if __name__ == "__main__":
    main()
