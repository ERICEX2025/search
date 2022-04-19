import sys
import xml.etree.ElementTree as et
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def indexer(xml_path: str, title_path: str, docs_path: str, words_path: str):
    # check how many arguments are passed in - print message if there are less than 4
    # (stop processing here?)

    # load the xml file into a tree and save root:
    root = et.parse(xml_path).getroot()

    # to iterate children nodes:
    for child in root:
        # whatever we want it to do
        pass

    # all pages:
    all_pages = root.findall("page")

    # iterate through all the pages:
    for page in all_pages:
        # do something
        pass

    # extracting the text of all children with a certain tag (this case as title)
    # might need to use .strip() if getting weird return
    titles = page.find('title').text

    # create new regex - i don't think this is the one we want to use
    n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''

    # finds all regex matches in string/file
    cool_tokens = re.findall(n_regex, "some string or file")

    for word in cool_tokens:
        # do something to each word
        pass

    # a set of stop words to use - can search for stop words over
    stop_words = set(stopwords.words('english'))

    # can stem a single word with make_stems.stem("word") - use a for loop to apply this to all words in corpus
    make_stems = PorterStemmer()
