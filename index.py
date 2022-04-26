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

        # pagerank
        self.previous = {}  # id --> rank r
        self.current = {}  # id --> rank r'

        # pagerank
        self.links_dict = {}
        # pagerank
        self.title_to_id = {}

        # title dic
        self.title_dict = {}

        self.parser()
        
        self.write_files()

    def parser(self):
        # xml
        self.root = et.parse(self.xml_path).getroot()
        # returns list of pages
        self.all_pages = self.root.findall("page")

        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stop_words = set(stopwords.words('english'))
        make_stems = PorterStemmer()
        # for linkDic
        link_regex = '''\[\[[^\[]+?\]\]'''

        # for every page
        for page in self.all_pages:
            #okay I think there is a problem here because if word has | it is unioned and then also added again and stemmed

            for word in all_text:
                word.strip("[[ ]]")
                # TODO deal with metapages
                if ":" in word:
                    word.split(":",)    
                elif "|" in word:
                    # WHAT ABOUT META PAGES! ah yes
                    # why union? and not just add.
                    # we need to keep track of the title as what the page links to, add it to the dictionary? somehow
                    self.word_corpus.union(re.findall(
                        n_regex, word[word.find("|")+1:]))  # look at
                elif word not in stop_words:
                    self.word_corpus.add(make_stems.stem(word.lower()))

            # loops through each page and adds page id and title to the title dic
            self.title_dict[int(page.find('id').text)] = page.find(
                'title').text.strip()

            self.title_to_id[page.find('title').text] = int(
                page.find('id').text)

            all_text = re.findall(n_regex, page.find('text').text)
            all_titles = re.findall(n_regex, page.find('title').text)
            all_text.extend(all_titles)


        for page in self.all_pages:
            self.links_dict[int(page.find('id').text)] = set()
            all_links = re.findall(link_regex, page.find('text').text)
            for link in all_links:
                stripped_link = link.strip("[[ ]]")
                if "|" in stripped_link:
                    self.links_dict[int(page.find('id').text)].add(
                        self.title_to_id[stripped_link.partition("|")[0]])
                else:
                    self.links_dict[int(page.find('id').text)].add(
                        self.title_to_id[stripped_link])

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
        file_io.write_title_file(
            self.title_path, self.title_dict) #writing to title but not to the other two?
        file_io.write_words_file(self.words_path, self.relevance_dict)
        file_io.write_docs_file(self.docs_path, self.current)


if __name__ == "__main__":
    if(len(sys.argv)-1 != 4):  # -1 cause the name of the script (e.g. "index.py")... can usually ignore
        print("Wrong number of arguments!!!")
    else:
        Indexer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
