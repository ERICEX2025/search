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

    def querier(self):

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

        return tot_sum

    def page_rank_score(self):
        tot_sum = {}  # from id to sum value
        for page in self.title_dict:
            tot_sum[int(page.find('id').text)] = 0
            for word in self.query:
                tot_sum[int(page.find('id').text)] += (self.words_dict[word]
                                                       [int(page.find('id').text)] * self.docs_dict[int(page.find('id').text)])

        return tot_sum


# main method should support the following:
# python3 query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>
if __name__ == "__main__":
    while True:
        query = input("What would you like to search:")
        if query == ":quit":
            break
        if (len(sys.argv) == 5):
            # include page rank - call helper
            pass
        elif (len(sys.argv) == 4):
            # no page rank - call helper
            pass
        else:
            raise ValueError("invalid number of args")

        # return the document titles in order of priority (might need a line to print 1-10 in front of doc name)
    exit
