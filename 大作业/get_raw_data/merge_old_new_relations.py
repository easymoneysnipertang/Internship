import os

if __name__ == '__main__':
    filename1_end = './data1/relations.txt'
    filename2_start = './data1/extent_relations_clean.txt'

    all_sentences_set = set()
    with open(filename1_end, "r", encoding="utf-8") as fr:
        for line in fr:
            sentence = line.strip()
            all_sentences_set.add(sentence)

    with open(filename2_start, "r", encoding="utf-8") as fr:
        for line in fr:
            sentence = line.strip()
            all_sentences_set.add(sentence)


    with open(filename1_end, 'w', encoding='utf-8') as fw:
        for line in all_sentences_set:
            fw.write(line + '\n')


