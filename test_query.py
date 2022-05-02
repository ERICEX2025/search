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
    c.handle_query("A")
    assert c.title_dict == {1: "A", 2: "B", 3: "C"}
    assert c.docs_dict == {1: 0.4326427188659158,
                           2: 0.23402394780075067, 3: 0.33333333333333326}
    assert c.words_dict == {"a": {1: 1.0986122886681098},
                            "b": {1: 0.4054651081081644, 2: 0.4054651081081644},
                            "c": {1: 0.4054651081081644, 3: 0.4054651081081644},
                            "f": {3: 1.0986122886681098}}
    assert c.query_corpus == {"a"}
    assert c.title_list == ["A"]


"""Tests query when page rank is not included"""


def test_query_page_rank2():
    d = query.Querier("txt-files/titles4.txt",
                      "txt-files/docs4.txt", "txt-files/words4.txt", False)
    d.handle_query("A")
    assert d.query_corpus == {"a"}
    assert d.title_list == ["A", "D"]


"""Tests query when a query produces no results"""


def test_query_page_rank3():
    e = query.Querier("txt-files/titles5.txt",
                      "txt-files/docs5.txt", "txt-files/words5.txt", True)
    assert e.handle_query("no words") == "no results were found!"
