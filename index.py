import sys
import xml.etree.ElementTree as et
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
import file_io


class Indexer:
    """Indexer class gets called from the main
    to parse wifi files and write to txt files for
    Query to use
    """

    def __init__(self, xml: str, title: str, doc: str, word: str):
        """Constructor for Indexer

        Parameters:
        xml -- the first number
        y -- the second number
        
        Returns:
        A number (the sum of x and y)
        
        Throws: 
        BadInputError if x or y (or both) is not a number
        """
        # instaniating variabling our given input and output files
        self.xml_path = xml
        self.title_path = title
        self.docs_path = doc
        self.words_path = word

        # title dic: id to title
        self.id_title_dict = {}
        self.title_id_dict = {}
        # relevance dic: words to dic of pages to relevance
        self.relevance_dict = {}
        # pagerank id to title will there be multiple pages that have the same title?
        self.links_dict = {}
        # pagerank calculation
        self.previous = {}  # id --> rank r
        self.current = {}  # id --> rank r'

        # xml is the root
        root = et.parse(self.xml_path).getroot()
        self.all_pages = root.findall("page")
        self.num_of_pages = len(self.all_pages)

        self.setup()
        self.parser()
        self.idf()
        self.page_rank()
        self.write_files()

    def setup(self):
        for page in self.all_pages:
            page_id = int(page.find('id').text)
            title = page.find('title').text.strip
            self.previous[page_id] = 0
            self.current[page_id] = 1/self.num_of_pages
            # for title dic loops through each page and adds page id to coresponding title
            self.id_title_dict[page_id] = title
            self.title_id_dict[title] = page_id

    def parser(self):
        '''Populates the rel dic: dictionary of words to dictionary of documents to relevance
        '''
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stop_words = set(stopwords.words('english'))
        make_stems = PorterStemmer()

        for page in self.all_pages:
            page_id = int(page.find('id').text)
            title = page.find('title').text
            # for title dic loops through each page and adds page id to coresponding title
            self.id_title_dict[page_id] = title.strip()
            # for pagerank keep track of id to set of pages (through their title)
            self.links_dict[page_id] = set()
            # for tf max count for a word
            aj_max_count = 1
            set_of_words_in_this_page = set()
            title_text = re.findall(n_regex, title)
            all_text = re.findall(n_regex, page.find('text').text)
            all_text.extend(title_text)

            for word in all_text:
                is_link = False
                if "[[" in word and "]]" in word:
                    is_link = True
                stripped_word = word.strip("[[ ]]")
                # case |
                if "|" in stripped_word:
                    if stripped_word[0:stripped_word.find("|")] in self.title_id_dict\
                        and self.title_id_dict[stripped_word[0:stripped_word.find("|")]] != page_id:
                        self.links_dict[page_id].add(
                            self.title_id_dict[stripped_word[:stripped_word.find("|")]])
                    list = re.findall(
                        n_regex, stripped_word[stripped_word.find("|") + 1:])
                # case :
                elif ":" in stripped_word or is_link:
                    if stripped_word in self.title_id_dict and self.title_id_dict[stripped_word] != page_id:
                        self.links_dict[page_id].add(
                            self.title_id_dict[stripped_word])
                    list = re.findall(n_regex, stripped_word)
                # case not link
                else:
                    list = [stripped_word]
                for wrd in list:
                    if wrd not in stop_words:
                        lower_stemmed_word = make_stems.stem(wrd.lower())
                        set_of_words_in_this_page.add(lower_stemmed_word)
                        if lower_stemmed_word not in self.relevance_dict:
                            initialize_dic = {}
                            initialize_dic[page_id] = 1
                            # initialize with count 1
                            self.relevance_dict[lower_stemmed_word] = initialize_dic
                        else:
                            if page_id in self.relevance_dict[lower_stemmed_word]:
                                # add count
                                self.relevance_dict[lower_stemmed_word][page_id] += 1
                            else:
                                self.relevance_dict[lower_stemmed_word][page_id] = 1
                            if self.relevance_dict[lower_stemmed_word][page_id] >= aj_max_count:
                                aj_max_count = self.relevance_dict[lower_stemmed_word][page_id]
            # populate with tf
            for wordd in set_of_words_in_this_page:
                tf = self.relevance_dict[wordd][page_id]/aj_max_count

    def idf(self):
        # populate with idf
        for word in self.relevance_dict:
            num_of_page_for_word = len(self.relevance_dict[word])
            for doc in self.relevance_dict[word]:
                self.relevance_dict[word][doc] *= math.log(
                    self.num_of_pages/num_of_page_for_word)

    def page_rank(self):
        while self.compute_dist(self.current, self.previous) > .001:
            self.previous = self.current.copy()
            for j in self.all_pages:
                self.current[int(j.find('id').text)] = 0
                for k in self.all_pages:
                    self.current[int(j.find('id').text)] += self.compute_weights(
                        k, j) * self.previous[int(k.find('id').text)]
                    print(self.current)

    def compute_dist(self, previous: dict, current: dict):
        prev = []
        curr = []
        for key in previous:
            prev.append(previous[key])
        for key in current:
            curr.append(current[key])
        return math.dist(curr, prev)

    def compute_weights(self, page1: str, page2: str):
        page1_id = int(page1.find('id').text)
        page2_id = int(page2.find('id').text)
        if page1_id == page2_id:
            return 0.15/self.num_of_pages
        if len(self.links_dict[page1_id]) == 0:
            return 0.15/self.num_of_pages + (1 - 0.15)*(1/(self.num_of_pages - 1))
        elif page2_id in self.links_dict[page1_id]:
            return 0.15/self.num_of_pages + (1 - 0.15)*(1/len(self.links_dict[page1_id]))
        elif page2_id not in self.links_dict[page1_id]:
            return 0.15/self.num_of_pages

    def write_files(self):
        file_io.write_title_file(self.title_path, self.id_title_dict)
        file_io.write_words_file(self.words_path, self.relevance_dict)
        file_io.write_docs_file(self.docs_path, self.current)



if __name__ == "__main__":
    """Main method that handles the inputs for indexer
    prints "Wrong number of arguments!!!" if there aren't 4 arguments passed in

    Parameters:
    wiki xml file
    title text file
    doc text file
    word text file
    """
    
    if(len(sys.argv)-1 != 4):  # -1 cause the name of the script (e.g. "index.py")... can usually ignore
        print("Wrong number of arguments!!!")
    else:
        Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])