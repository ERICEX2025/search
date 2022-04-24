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
        self.xml_path = xml
        self.title_path = title
        self.docs_path = doc
        self.words_path = word

        self.word_corpus = set()
        self.relevance_dict = {}

        self.root = et.parse(self.xml_path).getroot()
        self.all_pages = self.root.findall("page")
        # Why don't we import all the words into the corpus here and pass it into parser

        self.previous = {}  # id --> rank r
        self.current = {}  # id --> rank r'

        self.links_dict = {}
        self.title_dict = {}

        self.parser()
        self.write_files()

    #I think we should have helper methods to split this up
    def parser(self):
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stop_words = set(stopwords.words('english'))
        make_stems = PorterStemmer()
        link_regex = '''\[\[[^\[]+?\]\]'''

        for page in self.all_pages:
            print(page.find('title').text) # is this for testing, (talking to myself) if so can get rid of
            all_text = re.findall(n_regex, page.find('text').text) 

            #loops through each page and adds page id and title to the title dic
            self.title_dict[int(page.find('id').text)] = page.find('title').text.strip() 

            for word in all_text:
                word.strip("[[ ]]") # what happens if the word doesn't have [[]] aka not a link
                if "|" in word:
                    # why union? and not just add. 
                    # we need to keep track of the title as what the page links to, add it to the dictionary? somehow
                    self.word_corpus.union(re.findall( 
                        n_regex, word[word.find("|")+1:]))
                if word not in stop_words:
                    self.word_corpus.add(make_stems.stem(word.lower()))

        for page in self.all_pages:
            self.links_dict[int(page.find('id').text)] = set()
            all_links = re.findall(link_regex, page.find('text').text)
            for link in all_links:
                stripped_link = link.strip("[[ ]]")
                if "|" in stripped_link:
                    self.links_dict[int(page.find('id').text)].add(
                        self.title_dict[stripped_link.partition("|")[0]]) #ask about and fix!!
                else:
                    self.links_dict[int(page.find('id').text)].add(
                        self.title_dict[stripped_link]) #ask about and fix!!

    def determine_tf(self):
        count_dict = {}  # word --> (id --> count)
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        make_stems = PorterStemmer()

        for word in self.word_corpus:
            count_dict[word] = {}
            for page in self.all_pages:
                count_dict[word][int(page.find('id').text)] = 0

        for page in self.all_pages:
            all_text = re.findall(n_regex, page.find('text').text)
            for word in all_text:
                if make_stems.stem(word) in self.word_corpus:
                    count_dict[make_stems.stem(word)][int(
                        page.find('id').text)] += 1

        max_list = {}
        for key in count_dict:
            for id in count_dict[key]:
                max_list[id] = 0

        for key in count_dict:
            for id in count_dict[key]:
                if count_dict[key][id] > max_list[id]:
                    max_list[id] = count_dict[key][id]

        for word in self.word_corpus:
            self.relevance_dict[word] = {}

        for page in self.all_pages:
            for word in self.word_corpus:
                self.relevance_dict[word][int(page.find('id').text)] = count_dict[word][int(
                    page.find('id').text)]/max_list[int(page.find('id').text)]

        return self.relevance_dict

    def determine_idf(self):
        doc_count = {}
        for word in self.word_corpus:
            doc_count[word] = 0
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        make_stems = PorterStemmer()

        for page in self.all_pages:
            all_text = set(re.findall(n_regex, page.find('text').text))
            for word in all_text:
                if make_stems.stem(word) in self.word_corpus:
                    doc_count[make_stems.stem(word)] += 1

        n = len(self.all_pages)

        for word in self.word_corpus:
            doc_count[word] = math.log(n/doc_count[word])

        return doc_count

    def determine_relevance(self):  # might do this is separate step

        idf_dict = self.determine_idf()
        for key in idf_dict:
            for page in self.all_pages:
                self.relevance_dict[key][int(page.find('id').text)] = self.relevance_dict[
                    key][int(page.find('id').text)] * idf_dict[key]












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
            print("first case", page1, page2)
            return 0.15/len(self.all_pages)
        elif len(self.links_dict[int(page1.find('id').text)]) == 0:
            print("second")
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
        file_io.write_title_file(
            self.title_path, self.title_dict)
        file_io.write_words_file(self.words_path, self.relevance_dict)
        file_io.write_document_file(self.docs_path, self.current)

if __name__ == "__main__":
    if(len(sys.argv)-1 != 4):  # -1 cause the name of the script (e.g. "index.py")... can usually ignore
        print("Wrong number of arguments!!!")
    else:
        Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])