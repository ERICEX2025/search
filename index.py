import sys
# from turtle import title
import xml.etree.ElementTree as et
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
import file_io

# OPTIMIZE LATER


class Indexer:

    def __init__(self, xml_path: str, title_path: str, docs_path: str, words_path: str):
        self.xml_path = xml_path
        self.title_path = title_path
        self.docs_path = docs_path
        self.words_path = words_path

        self.word_corpus = set()
        self.relevance_dict = {}

        self.root = et.parse(self.xml_path).getroot()
        self.all_pages = self.root.findall("page")

        self.previous = {}  # id --> rank r
        self.current = {}  # id --> rank r'

        self.parser()

    def indexer(self):
        if (len(sys.argv) != 4):
            raise ValueError("invalid number of arguments")

        # dict from page titles to page ids
        title_dict = {}
        for page in self.all_pages:
            title_dict[page.find('title').text] = int(page.find('id').text)

        # dict from ids to page rank

        file_io.write_title_file(
            self.title_path, title_dict)  # put in dicts here
        file_io.write_words_file(self.words_path, self.relevance_dict)
        file_io.write_document_file(self.docs_path, self.current)

    def parser(self):
        # remove some of these to make space?
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        stop_words = set(stopwords.words('english'))
        make_stems = PorterStemmer()

        for page in self.all_pages:  # faster way to do this?
            all_text = re.findall(n_regex, page.find('text').text)
            for word in all_text:
                if word not in stop_words:
                    self.word_corpus.add(make_stems.stem(word))

    def determine_tf(self):
        # have many dicts for now and optimize later

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

        max_list = {}  # make array if possible? dict ok?
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
                self.relevance_dict[(key, int(page.find('id').text))] = self.relevance_dict[(
                    key, int(page.find('id').text))] * idf_dict[key]

    def page_rank(self):

        for page in self.all_pages:
            self.previous[int(page.find('id').text)] = 0

        for page in self.all_pages:
            self.current[int(page.find('id').text)] = 1/len(self.all_pages)

        while self.compute_dist(self.previous, self.current) > .001:
            self.previous = self.current.copy()
            for j in self.all_pages:
                self.current[j] = 0
                for k in self.all_pages:
                    self.current[j] += self.compute_weights[(
                        k, j)] * self.previous[k]

    def compute_weights(self):
        # dict from (id, id) tuple --> weight
        weight_dict = {}
        for page1 in self.all_pages:
            for page2 in self.all_pages:
                weight_dict[(int(page1.find('id').text),
                             int(page2.find('id').text))] = 0

        # pseudocode:
        # if (page links to itself or to a page outside corpus):
        # do nothing (doesn't need to be a line but keep in mind)
        # elif (k has links to nothing)
        # e/n + (1 - e)(1/n-1)
        # elif (k links to j one or more times):
        # e/n + (1 - e)(1/unique number of links out of k)
        # elif (k does not link to j)
        # e/n
        pass

    def compute_dist(self, previous: dict, current: dict):
        prev = previous.values
        curr = current.values
        math.dist(curr - prev)
