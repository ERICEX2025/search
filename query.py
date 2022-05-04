from re import M
import sys
import file_io
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


class Querier:
    """Querier class gets called from the main
    to REPL and based on the user input, prints
    top 10 docs or no results were found!

    Throws:
    Invalid ValueError when the inputs are less 
    than 4 or greater 5
    """

    def __init__(self, title_path: str, docs_path: str, words_path: str, pg_rank: bool):
        """Constructor for Query
        initializes variables

        Parameters:
        title_path -- the title.txt document to read from
        doc_path -- the doc.txt document to read from
        word_path -- the word.txt document to read from
        """
        self.title_path = title_path
        self.docs_path = docs_path
        self.words_path = words_path
        self.pg_rank = pg_rank

        # empty dics to get filled from reading the inputted files
        self.title_dict = {}
        self.docs_dict = {}
        self.words_dict = {}

        # set of the query words
        self.query_corpus = set()
        # top 10 list to output
        self.title_list = []

        self.read_files()

    def read_files(self):
        """ Reads from the given files using file.io methods
        takes in the empty dictionaries that will be filled 
        based on the given txt files through the filo.io methods
        """
        file_io.read_title_file(self.title_path, self.title_dict)
        file_io.read_docs_file(self.docs_path, self.docs_dict)
        file_io.read_words_file(self.words_path, self.words_dict)

    def relevance_score(self):
        """ sums up the relevance value or relevance value 
        with pagerank for each page id and sort it based on 
        the most relevant, then add the title of the id in 
        that sorted order to the top 10 titlelist
        """
        tot_sum = {}  # from id to sum value
        # goes through each word of the query
        if self.pg_rank:
            self.page_rank_score(tot_sum)
        else:
            self.no_page_rank_score(tot_sum)

        sorted_dict = {k: v for k, v in sorted(
            tot_sum.items(), key=lambda item: item[1], reverse=True)}

        for id in list(sorted_dict.keys())[:10]:
            self.title_list.append(self.title_dict[id])

        if len(self.title_list) == 0:
            print("no results were found!")

    def page_rank_score(self, tot_sum: dict):
        """ Calculates the sum rel score for each 
        page id

        Parameters:
        tot_sum -- takes in the tot_sum dictionary to add to
        """
        for word in self.query_corpus:
            # if the words appear in the wiki page
            if word in self.words_dict:
                # loop through the ids that contain the word
                # add their corresponding rel value*pagerank
                # value to dic of ids to their sum rel value
                for key in self.words_dict[word]:
                    tot_sum[key] = 0
                    tot_sum[key] += (self.words_dict[word]
                                     [key] * self.docs_dict[key])

    def no_page_rank_score(self, tot_sum: dict):
        """ Calculates the sum rel score for each 
        page id including pagerank

        Parameters:
        tot_sum -- takes in the tot_sum dictionary to add to
        """
        for word in self.query_corpus:
            # if the words appear in the wiki page
            if word in self.words_dict:
                # loop through the ids that contain the word
                # add their corresponding rel value to dic
                # of ids to their sum rel value
                for key in self.words_dict[word]:
                    tot_sum[key] = 0
                    tot_sum[key] += self.words_dict[word][key]

    def print_list(self):
        """ Prints up to the top 10 pages to the user
        """
        for x in range(0, len(self.title_list)):
            print(str(x + 1) + ":" + self.title_list[x])

    def handle_query(self, query: str):
        """processes the query by adding
        to the query set and then calling
        page_rank_score() or relevance_score()
        based on if they inputted pagerank
        then prints the results

        Parameters:
        query -- the inputted query
        """
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stop_words = set(stopwords.words('english'))
        make_stems = PorterStemmer()

        # resets these lists for the next query
        self.query_corpus = set()
        self.title_list = []

        # processes the query, removing stop words and stems
        all_text = re.findall(n_regex, query)
        for word in all_text:
            if word not in stop_words:
                self.query_corpus.add(make_stems.stem(word.lower()))

        self.relevance_score()

        self.print_list()


if __name__ == "__main__":
    """Main method that handles the inputs for Query
    after inputting the correct arguments,
    constantly asks for a query and either returns
    no results were found or a list of top 10 documents
    until user inputs :quit

    Parameters:
    pagerank boolean
    title text file
    doc text file
    word text file

    Throws:
    Value Error if there are more than 5 or less than 4 arguments passed in
    """

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
