import pytest
import index

# why is this simple test not working ;(
# I will camp at conceptual hours and get this working and


def test_exception():
    """ tests invalid input """
    invalid_Length = [0]
    with pytest.raises(ValueError):
        test = index.Indexer(invalid_Length)  # not sure this will work...


# have a case when relevance is the same?
def test_index_tf_idf():
    a = index.Indexer("test_tf_idf.xml", "titles.txt", "docs.txt", "words.txt")
    assert a.title_dict is {1: 'Page 1', 2: 'Page 2', 3: 'Page 3'}
    assert a.relevance_dict is {'dog': {1: 0.4054651081081644, 2: 0.4054651081081644},
                                'bit': {1: 0.4054651081081644, 3: 0.2027325540540822},
                                'man': {1: 1.0986122886681098},
                                'page': {1: 0.0, 2: 0.0, 3: 0.0},
                                '1': {1: 1.0986122886681098},
                                'ate': {2: 1.0986122886681098},
                                'chees': {2: 0.4054651081081644, 3: 0.4054651081081644},
                                '2': {2: 1.0986122886681098},
                                '3': {3: 0.5493061443340549}}
    assert a.links_dict is {1: set(), 2: set(), 3: set()}
    assert a.current is {1: 0.3333333333333333,
                         2: 0.3333333333333333, 3: 0.3333333333333333}


def test_index_page_rank():
    b = index.Indexer("PageRankExample1.xml", "titles2.txt",
                      "docs2.txt", "words2.txt")
    assert b.title_dict is {1: 'A', 2: 'B', 3: 'C'}
    assert b.relevance_dict is {'A': {1: 1.0986122886681098},
                                'B': {1: 0.4054651081081644, 2: 0.4054651081081644},
                                'C': {1: 0.4054651081081644, 3: 0.4054651081081644},
                                'F': {3: 1.0986122886681098}}
    assert b.links_dict is {1: set('B', 'C'), 2: set(), 3: set('A')}
    assert b.current is {1: 0.4326, 2: 0.2340, 3: 0.3333}


def test_index_invalid_args():
    pass
    # not sure how to test this
