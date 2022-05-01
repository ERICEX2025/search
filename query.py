from re import M
import sys
import file_io
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# READ ME


class Querier:

    def __init__(self, title_path: str, docs_path: str, words_path: str, pg_rank: bool):
        self.title_path = title_path
        self.docs_path = docs_path
        self.words_path = words_path
        self.pg_rank = pg_rank

        self.title_dict = {}
        self.docs_dict = {}
        self.words_dict = {}

        self.query_corpus = set()

        self.title_list = []

        self.read_files()

    def read_files(self):

        file_io.read_title_file(self.title_path, self.title_dict)
        file_io.read_docs_file(self.docs_path, self.docs_dict)
        file_io.read_words_file(self.words_path, self.words_dict)

    def relevance_score(self):
        tot_sum = {}  # from id to sum value

        for word in self.query_corpus:  # fix key error - ask
            if word in self.words_dict:
                for key in self.words_dict[word]:
                    tot_sum[key] = 0
                    tot_sum[key] += self.words_dict[word][key]

        sorted_dict = {k: v for k, v in sorted(
            tot_sum.items(), key=lambda item: item[1], reverse=True)}

        for id in list(sorted_dict.keys())[:10]:
            self.title_list.append(self.title_dict[id])  # reset each time?

        if len(self.title_list) == 0:
            print("no results were found!")  # not an error - print statement

    def page_rank_score(self):
        tot_sum = {}  # from id to sum value
        for word in self.query_corpus:
            if word in self.words_dict:
                for key in self.words_dict[word]:
                    tot_sum[int(key.find('id').text)] = 0
                    tot_sum[int(key.find('id').text)] += (self.words_dict[word]
                                                          [int(key.find('id').text)] * self.docs_dict[int(key.find('id').text)])

        sorted_dict = {k: v for k, v in sorted(
            tot_sum.items(), key=lambda item: item[1], reverse=True)}

        for id in list(sorted_dict.keys())[:10]:
            self.title_list.append(self.title_dict[id])

        if len(self.title_list) == 0:
            raise ValueError("no results were found!")

    def print_list(self):
        for x in range(0, len(self.title_list)):
            print(str(x + 1) + ":" + self.title_list[x])

    def handle_query(self, query: str):
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stop_words = set(stopwords.words('english'))
        make_stems = PorterStemmer()

        self.query_corpus = set()

        all_text = re.findall(n_regex, query)
        for word in all_text:
            if word not in stop_words:
                self.query_corpus.add(make_stems.stem(word.lower()))

        if self.pg_rank == True:
            self.page_rank_score()
        elif self.pg_rank == False:
            self.relevance_score()

        self.print_list()


if __name__ == "__main__":
    q = None
    if (len(sys.argv) == 5):
        q = Querier(sys.argv[2], sys.argv[3], sys.argv[4], True)
    elif (len(sys.argv) == 4):
        q = Querier(sys.argv[1], sys.argv[2], sys.argv[3], False)
    else:
        raise ValueError("invalid number of args")

    while True:
        query = input("What would you like to search:")
        if query == ":quit":
            break
        q.handle_query(query)
