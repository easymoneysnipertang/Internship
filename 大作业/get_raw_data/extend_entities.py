import os

def read_file_to_set(filename):
    temp_set = set()
    with open(filename, "r", encoding="utf-8") as fr:
        for line in fr:
            words = line.strip().split()
            if len(words) == 3 and words[1]!='从属':
                temp_set.add(words[2])
    return temp_set


def write_set_to_file(words_set, output_file):
    with open(output_file, 'w', encoding='utf-8') as fw:
        for word in words_set:
            fw.write(word + '\n')


if __name__ == '__main__':
    input_file_name = './data1/relations.txt'
    output_file_name = './data1/extent_entities.txt'
    os.makedirs(os.path.dirname(output_file_name), exist_ok=True)
    first_words_set = read_file_to_set(input_file_name)

    all_words_set = set()
    with open(input_file_name, "r", encoding="utf-8") as fr:
        for line in fr:
            words = line.strip().split()
            if len(words) == 3:
                all_words_set.add(words[0])

    new_words_set = first_words_set.difference(all_words_set)
    write_set_to_file(new_words_set, output_file_name)
