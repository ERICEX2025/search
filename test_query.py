import pytest
import query

# make different txt files


def test_query_tf_idf():
    a = query.Querier("titles.txt", "docs.txt", "words.txt", False)
    a.handle_query("dog eat man")
    assert a.title_dict is {1: 'Page 1', 2: 'Page 2', 3: 'Page 3'}
    assert a.docs_dict is {1: 0.3333333333333333,
                           2: 0.3333333333333333, 3: 0.3333333333333333}
    assert a.words_dict is {'dog': {1: 0.4054651081081644, 2: 0.4054651081081644},
                            'bit': {1: 0.4054651081081644, 3: 0.2027325540540822},
                            'man': {1: 1.0986122886681098},
                            'page': {1: 0.0, 2: 0.0, 3: 0.0},
                            '1': {1: 1.0986122886681098},
                            'ate': {2: 1.0986122886681098},
                            'chees': {2: 0.4054651081081644, 3: 0.4054651081081644},
                            '2': {2: 1.0986122886681098},
                            '3': {3: 0.5493061443340549}}
    assert a.query_corpus is {"dog", "eat", "man"}
    assert a.title_list is ['Page 1', 'Page 2']


def test_query_page_rank():
    b = query.Querier("titles2.txt", "docs2.txt", "words2.txt", True)
    b.handle_query("A")
    assert b.title_dict is {1: 'A', 2: 'B', 3: 'C'}
    assert b.docs_dict is {1: 0.4326, 2: 0.2340, 3: 0.3333}
    assert b.words_dict is {'A': {1: 1.0986122886681098},
                            'B': {1: 0.4054651081081644, 2: 0.4054651081081644},
                            'C': {1: 0.4054651081081644, 3: 0.4054651081081644},
                            'F': {3: 1.0986122886681098}}
    assert b.query_corpus is {"A"}
    assert b.title_list is 
