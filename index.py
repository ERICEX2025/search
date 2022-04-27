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

        self.relevance_dict = {}

        # # pagerank
        # self.previous = {}  # id --> rank r
        # self.current = {}  # id --> rank r'

        # # pagerank
        # self.links_dict = {}
        # # pagerank
        # self.title_to_id = {}

        # # title dic
        # self.title_dict = {}

        self.parser()
        # self.page_rank()
        self.write_files()

    def parser(self):
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stop_words = set(stopwords.words('english'))
        make_stems = PorterStemmer()
        # link_regex = '''\[\[[^\[]+?\]\]'''

        # xml is the root
        self.root = et.parse(self.xml_path).getroot()
        self.all_pages = self.root.findall("page")
        
        num_of_pages = 0
        for page in self.all_pages:
            # for tf
            aj_max_count = 0
            set_of_words_in_this_page = set()
            title = re.findall(n_regex, page.find('title').text)
            all_text = re.findall(n_regex, page.find('text').text)
            all_text.extend(title)
            page_id = int(page.find('id').text)
            for word in all_text:
                # strip links
                word.strip("[[ ]]")
                if word in stop_words:
                    continue
                # case |
                elif "|" in word:
                    list = re.findall(n_regex, word[word.find("|") + 1:])  
                # case :
                elif ":" in word:
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
            for wordd in set_of_words_in_this_page:
                tf = self.relevance_dict[wordd][page_id]/aj_max_count
                self.relevance_dict[wordd][page_id] = tf 
            num_of_pages += 1
        for word in self.relevance_dict:
            num_of_page_for_word = len(self.relevance_dict[word])
            for doc in self.relevance_dict[word]:
                self.relevance_dict[word][doc] *= math.log(num_of_pages/num_of_page_for_word)


            # loops through each page and adds page id and title to the title dic
            # self.title_dict[int(page.find('id').text)] = page.find(
            #     'title').text.strip()

            # self.title_to_id[page.find('title').text] = int(
            #     page.find('id').text)

            # self.links_dict[int(page.find('id').text)] = set()
            # all_links = re.findall(link_regex, page.find('text').text)
            # for link in all_links:
            #     stripped_link = link.strip("[[ ]]")
            #     if "|" in stripped_link:
            #         self.links_dict[int(page.find('id').text)].add(
            #             self.title_to_id[stripped_link.partition("|")[0]])
            #     else:
            #         self.links_dict[int(page.find('id').text)].add(
            #             self.title_to_id[stripped_link])


    def page_rank(self):

        for page in self.all_pages:
            self.previous[int(page.find('id').text)] = 0

        for page in self.all_pages:
            self.current[int(page.find('id').text)] = 1/len(self.all_pages)

        while self.compute_dist(self.current, self.previous) > .001:
            self.previous = self.current.copy()
            for j in self.all_pages:
                self.current[int(j.find('id').text)] = 0
                for k in self.all_pages:
                    self.current[int(j.find('id').text)] += self.compute_weights(
                        k, j) * self.previous[int(k.find('id').text)]

    def compute_weights(self, page1: str, page2: str):

        if int(page1.find('id').text) == int(page2.find('id').text):
            return 0.15/len(self.all_pages)
        elif len(self.links_dict[int(page1.find('id').text)]) == 0:
            return 0.15/len(self.all_pages) + (1 - 0.15)*(1/(len(self.all_pages) - 1))
        elif int(page2.find('id').text) in self.links_dict[int(page1.find('id').text)]:
            return 0.15/len(self.all_pages) + (1 - 0.15)*(1/len(self.links_dict[int(page1.find('id').text)]))
        elif int(page2.find('id').text) not in self.links_dict[int(page1.find('id').text)]:
            return 0.15/len(self.all_pages)

    def compute_dist(self, previous: dict, current: dict):
        prev = []
        curr = []
        for key in previous:
            prev.append(previous[key])
        for key in current:
            curr.append(current[key])
        return math.dist(curr, prev)

    def write_files(self):
        # file_io.write_title_file(
        #     self.title_path, self.title_dict)  # writing to title but not to the other two?
        file_io.write_words_file(self.words_path, self.relevance_dict)
        # file_io.write_docs_file(self.docs_path, self.current)


if __name__ == "__main__":
    if(len(sys.argv)-1 != 4):  # -1 cause the name of the script (e.g. "index.py")... can usually ignore
        print("Wrong number of arguments!!!")
    else:
        Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])