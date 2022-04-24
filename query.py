from re import M
import sys
import file_io

# where is the query? sys.argv?
# where to rank


class Querier:

    def __init__(self, title_path: str, docs_path: str, words_path: str):
        self.title_path = title_path
        self.docs_path = docs_path
        self.words_path = words_path

        self.title_dict = {}
        self.docs_dict = {}
        self.words_dict = {}

        self.query = []  # figure out how to populate this

        # need to parse input in main - how and where

        # if no results, print a message

    def read_files(self):

        file_io.read_title_file(self.title_path, self.title_dict)
        file_io.read_docs_file(self.docs_path, self.docs_dict)
        file_io.read_words_file(self.words_path, self.words_dict)

    def relevance_score(self):
        tot_sum = {}  # from id to sum value
        for page in self.title_dict:
            tot_sum[int(page.find('id').text)] = 0
            for word in self.query:
                tot_sum[int(page.find('id').text)
                        ] += self.words_dict[word][int(page.find('id').text)]

        sorted(tot_sum.values(), reverse=True)
        sorted_dict = {}

        for i in sorted(tot_sum.values(), reverse=True):
            for k in tot_sum.keys():
                if tot_sum[k] == i:
                    sorted_dict[k] = tot_sum[k]

        title_list = []
        for id in list(sorted_dict.keys())[:10]:
            title_list.append(self.title_dict[id])

        return title_list

    def page_rank_score(self):
        tot_sum = {}  # from id to sum value
        for page in self.title_dict:
            tot_sum[int(page.find('id').text)] = 0
            for word in self.query:
                tot_sum[int(page.find('id').text)] += (self.words_dict[word]
                                                       [int(page.find('id').text)] * self.docs_dict[int(page.find('id').text)])

        sorted(tot_sum.values(), reverse=True)
        sorted_dict = {}

        for i in sorted(tot_sum.values(), reverse=True):
            for k in tot_sum.keys():
                if tot_sum[k] == i:
                    sorted_dict[k] = tot_sum[k]

        title_list = []
        for id in list(sorted_dict.keys())[:10]:
            title_list.append(self.title_dict[id])

        return title_list


# main method should support the following:
# python3 query.py[--pagerank] < titleIndex > <documentIndex > <wordIndex >
if __name__ == "__main__":
    while True:
        query = input("What would you like to search:")
        if query == ":quit":
            break
        if (len(sys.argv) == 5):
            # include page rank - call helper
            Querier(sys.argv[2], sys.argv[3], sys.argv[4]).page_rank_score()
        elif (len(sys.argv) == 4):
            # no page rank - call helper
            Querier(sys.argv[1], sys.argv[2], sys.argv[3]).relevance_score()
        else:
            raise ValueError("invalid number of args")
    exit
