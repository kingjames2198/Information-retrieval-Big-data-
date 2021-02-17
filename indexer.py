import os
import json
from pathlib import Path
import time

# a -> a b c d e
# b -> f g h i j
# d -> k l m n o
# e -> p q r s t
# f -> u v w x y z


def name(ch):
    if ch in 'abcdef':
        return 'a'
    elif ch in 'ghijkl':
        return 'g'
    elif ch in 'mnopqr':
        return 'm'
    else:
        return 's'


class Trie:
    def __init__(self):
        self.root = Path(__file__).resolve().parent / 'Trie'
        self.cache = dict()
        self.lru = list()
        self.max_size = 1000
        self.big_data = open('big.txt', 'w')

    def add(self, word, postings):
        if len(word) <= 2:
            return

        path = self.root / word[:2]
        for i in word[2:]:
            path = path / name(i)

        if not os.path.exists(path):
            os.makedirs(path)

        path = path / 'data.json'
        if not os.path.exists(path):
            # create a new file
            with open(path, 'w', encoding='utf-8') as pl:
                json.dump({word: postings}, pl)
            self.big_data.write(word)
        else:
            if path in self.cache:
                dict_list = self.cache[path]
                if word in dict_list:
                    dict_list[word].extend(postings)
                else:
                    dict_list[word] = postings
                    self.big_data.write(word)
                self.lru.remove(path)
                self.lru.insert(0, path)

            else:
                with open(path, 'r', encoding='utf-8') as rd:
                    dict_list = json.load(rd)
                    if word in dict_list:
                        dict_list[word].extend(postings)
                    else:
                        dict_list[word] = postings
                        self.big_data.write(word)
                self.cache[path] = dict_list
                self.lru.insert(0, path)

        if len(self.lru) > self.max_size:
            path = self.lru.pop(-1)
            with open(path, 'w', encoding='utf-8') as wrt:
                json.dump(self.cache[path], wrt)
            del self.cache[path]

    def get_postings(self, word):
        if len(word) <= 2:
            return None
        postings_path = self.root / word[:2]
        for i in word[2:]:
            postings_path = postings_path / name(i)

        postings_path = postings_path / 'data.json'
        if not os.path.exists(postings_path):
            return None
        else:
            with open(postings_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data[word]


T = Trie()


def create_index():
    start = time.time()
    for i in range(1, 10000):
        index = str(i)
        with open('Indexes/{index}.json'.format(index=index), 'r', encoding='utf-8') as clfile:
            x = json.load(clfile)
            for k in sorted(x):
                T.add(k, x[k])
        if i % 20 == 0:
            print(index, " : ", len(x), (time.time() - start))


def search(word: str):
    postings = T.get_postings(word)
    if postings is not None:
        for x in postings:
            print("docID is : ", x[0])


def get_posting_list(word: str):
    return T.get_postings(word)
