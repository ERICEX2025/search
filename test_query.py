import pytest
import query

"""Tests query for basic tf/idf case - no page rank"""


def test_query_tf_idf():
    a = query.Querier("txt-files/titles.txt",
                      "txt-files/docs.txt", "txt-files/words.txt", False)
    a.handle_query("dog eat man")
    assert a.title_dict == {1: "Page 1", 2: "Page 2", 3: "Page 3"}
    assert a.docs_dict == {1: 0.3333333333333333,
                           2: 0.3333333333333333, 3: 0.3333333333333333}
    assert a.words_dict == {"dog": {1: 0.4054651081081644, 2: 0.4054651081081644},
                            "bit": {1: 0.4054651081081644, 3: 0.2027325540540822},
                            "man": {1: 1.0986122886681098},
                            "page": {1: 0.0, 2: 0.0, 3: 0.0},
                            "1": {1: 1.0986122886681098},
                            "ate": {2: 1.0986122886681098},
                            "chees": {2: 0.4054651081081644, 3: 0.4054651081081644},
                            "2": {2: 1.0986122886681098},
                            "3": {3: 0.5493061443340549}}
    assert a.query_corpus == {"dog", "eat", "man"}
    assert a.title_list == ["Page 1", "Page 2"]


"""Tests query when page rank is included"""


def test_query_page_rank():
    c = query.Querier("txt-files/titles2.txt",
                      "txt-files/docs2.txt", "txt-files/words2.txt", True)
    c.handle_query("B")
    assert c.title_dict == {1: "A", 2: "B", 3: "C"}
    assert c.docs_dict == {1: 0.4326427188659158,
                           2: 0.23402394780075067, 3: 0.33333333333333326}
    assert c.words_dict == {"b": {1: 0.4054651081081644, 2: 0.4054651081081644},
                            "c": {1: 0.4054651081081644, 3: 0.4054651081081644},
                            "f": {3: 1.0986122886681098}}
    assert c.query_corpus == {"b"}
    assert c.title_list == ["A", "B"]


"""Tests query when page rank is not included and we are searching for a title"""


def test_query_title():
    d = query.Querier("txt-files/titles4.txt",
                      "txt-files/docs4.txt", "txt-files/words4.txt", False)
    d.handle_query("B")
    assert d.query_corpus == {"b"}
    assert d.title_list == ["B"]


"""Tests query when page rank is not included and we are searching for text"""


def test_query_text():
    d = query.Querier("txt-files/small_titles.txt",
                      "txt-files/small_docs.txt", "txt-files/small_words.txt", False)
    d.handle_query("example")
    assert d.query_corpus == {"exampl"}
    assert d.title_list == ['Macro-historical',
                            'Anatopism',
                            'Comparative historical research',
                            'Anachronism',
                            'Sinecure',
                            'Progressive war',
                            'Memory hole',
                            'Transformation of culture',
                            'Popular history',
                            'Loss exchange ratio']


"""Tests query when page rank is included and we are searching for a title"""


def test_query_title2():
    d = query.Querier("txt-files/titles4.txt",
                      "txt-files/docs4.txt", "txt-files/words4.txt", True)
    d.handle_query("C")
    assert d.query_corpus == {"c"}
    assert d.title_list == ["D", "C", "A"]


"""Tests query when page rank is included and we are searching for text"""


def test_query_text2():
    d = query.Querier("txt-files/small_titles.txt",
                      "txt-files/small_docs.txt", "txt-files/small_words.txt", True)
    d.handle_query("example")
    assert d.query_corpus == {"exampl"}
    assert d.title_list == ['Carthage',
                            'Memory hole',
                            'Anatopism',
                            'Loss exchange ratio',
                            'Anachronism',
                            'Tertullian',
                            'Rome',
                            'Macro-historical',
                            'Chronology',
                            'Comparative historical research']
