import sys
# from turtle import title
import xml.etree.ElementTree as et
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
import file_io

# OPTIMIZE LATER - limit the number of for loops (we loop through all of the pages a couple of times - try to combine)!!!


class Indexer:

    def __init__(self, xml: str, title: str, doc: str, word: str):
        #instance variabling our given input and output files
        self.xml_path = xml
        self.title_path = title
        self.docs_path = doc
        self.words_path = word

        # title dic: id to title
        self.title_dict = {}
        # relevance dic: words to dic of pages to relevance
        self.relevance_dict = {}
        # pagerank id to title will there be multiple pages that have the same title?
        self.links_dict = {}
        # id --> rank r'
        self.current = {} 

        self.parser()
        self.page_rank()
        self.write_files()

    def parser(self):
        '''Populates the rel dic: dictionary of words to dictionary of documents to relevance
        '''
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stop_words = set(stopwords.words('english'))
        make_stems = PorterStemmer()
        # link_regex = '''\[\[[^\[]+?\]\]'''

        # xml is the root
        self.root = et.parse(self.xml_path).getroot()
        self.all_pages = self.root.findall("page")
        
        self.num_of_pages = 0
        for page in self.all_pages:
            page_id = int(page.find('id').text)
            title = page.find('title').text

            # for title dic loops through each page and adds page id to coresponding title 
            self.title_dict[page_id] = title.strip()
            # for pagerank keep track of id to set of pages (through their title)
            self.links_dict[page_id] = set()
            # for tf max count for a word
            aj_max_count = 0
            set_of_words_in_this_page = set()

            title_text = re.findall(n_regex, title)
            all_text = re.findall(n_regex, page.find('text').text)
            all_text.extend(title_text)

            for word in all_text:
                # strip links
                word.strip("[[ ]]")
                if word in stop_words:
                    continue
                # case |
                elif "|" in word:
                    self.links_dict[page_id].add(word[:word.find("|")])
                    list = re.findall(n_regex, word[word.find("|") + 1:])  
                # case :
                elif ":" in word:
                    self.links_dict[page_id].add(word)
                    list = re.findall(n_regex, word)
                # case not link
                else:
                    list = [word]
                for wrd in list:
                    if wrd not in stop_words:
                        lower_stemmed_word = make_stems.stem(wrd.lower())
                        set_of_words_in_this_page.add(lower_stemmed_word)
                        if lower_stemmed_word not in self.relevance_dict:
                            initialize_dic = {}
                            initialize_dic[page_id] = 1
                            self.relevance_dict[lower_stemmed_word] = initialize_dic # initialize with count 1 
                            if aj_max_count == 0:
                                aj_max_count = 1
                        else:
                            if page_id in self.relevance_dict[lower_stemmed_word]:
                                self.relevance_dict[lower_stemmed_word][page_id] += 1 # add count 
                            else:
                                self.relevance_dict[lower_stemmed_word][page_id] = 1
                            if self.relevance_dict[lower_stemmed_word][page_id] >= aj_max_count:
                                aj_max_count = self.relevance_dict[lower_stemmed_word][page_id]
            # populate with tf                    
            for wordd in set_of_words_in_this_page:
                tf = self.relevance_dict[wordd][page_id]/aj_max_count
                self.relevance_dict[wordd][page_id] = tf 
            self.num_of_pages += 1
        #populate with idf included
        for word in self.relevance_dict:
            num_of_page_for_word = len(self.relevance_dict[word])
            for doc in self.relevance_dict[word]:
                self.relevance_dict[word][doc] *= math.log(self.num_of_pages/num_of_page_for_word)

    def page_rank(self):
        previous = {}  # id --> rank r
        for page in self.all_pages:
            previous[int(page.find('id').text)] = 0
            self.current[int(page.find('id').text)] = 1/len(self.all_pages)

        while self.compute_dist(self.current, previous) > .001:
            previous = self.current.copy()
            for j in self.all_pages:
                self.current[int(j.find('id').text)] = 0
                for k in self.all_pages:
                    self.current[int(j.find('id').text)] += self.compute_weights(
                        k, j) * previous[int(k.find('id').text)]

    def compute_weights(self, page1: str, page2: str):
        page1_id = int(page1.find('id').text)
        page2_id = int(page2.find('id').text)
        page2_title = page2.find('title').text
        if page1_id == page2_id:
            return 0.15/self.num_of_pages
        elif len(self.links_dict[page1_id]) == 0:
            return 0.15/self.num_of_pages + (1 - 0.15)*(1/(self.num_of_pages - 1))
        elif page2_title in self.links_dict[int(page1.find('id').text)]:
            return 0.15/self.num_of_pages + (1 - 0.15)*(1/len(self.links_dict[int(page1.find('id').text)]))
        elif page2_title not in self.links_dict[int(page1.find('id').text)]:
            return 0.15/self.num_of_pages

    def compute_dist(self, previous: dict, current: dict):
        prev = []
        curr = []
        for key in previous:
            prev.append(previous[key])
        for key in current:
            curr.append(current[key])
        return math.dist(curr, prev)

    def write_files(self):
        file_io.write_title_file(self.title_path, self.title_dict) 
        file_io.write_words_file(self.words_path, self.relevance_dict)
        file_io.write_docs_file(self.docs_path, self.current)


if __name__ == "__main__":
    if(len(sys.argv)-1 != 4):  # -1 cause the name of the script (e.g. "index.py")... can usually ignore
        print("Wrong number of arguments!!!")
    else:
        Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])