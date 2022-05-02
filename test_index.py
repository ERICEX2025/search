import pytest
import index

# why is this simple test not working ;(
# I will camp at conceptual hours and get this working and


# def test_exception():
#     """ tests invalid input """
#     invalid_Length = [0]
#     with pytest.raises(ValueError):
#         test = index.Indexer()  # not sure this will work...


# have a case when relevance is the same?
def test_index_tf_idf():
    a = index.Indexer("xml-files/test_tf_idf.xml",
                      "txt-files/titles.txt", "txt-files/docs.txt", "txt-files/words.txt")
    assert a.id_title_dict == {1: "Page 1", 2: "Page 2", 3: "Page 3"}
    assert a.relevance_dict == {"dog": {1: 0.4054651081081644, 2: 0.4054651081081644},
                                "bit": {1: 0.4054651081081644, 3: 0.2027325540540822},
                                "man": {1: 1.0986122886681098},
                                "page": {1: 0.0, 2: 0.0, 3: 0.0},
                                "1": {1: 1.0986122886681098},
                                "ate": {2: 1.0986122886681098},
                                "chees": {2: 0.4054651081081644, 3: 0.4054651081081644},
                                "2": {2: 1.0986122886681098},
                                "3": {3: 0.5493061443340549}}
    assert a.links_dict == {1: set(), 2: set(), 3: set()}
    assert a.current == {1: 0.3333333333333333,
                         2: 0.3333333333333333, 3: 0.3333333333333333}


def test_index_page_rank1():
    b = index.Indexer("xml-files/PageRankExample1.xml", "txt-files/titles2.txt",
                      "txt-files/docs2.txt", "txt-files/words2.txt")
    assert b.id_title_dict == {1: "A", 2: "B", 3: "C"}
    assert b.relevance_dict == {"b": {1: 0.4054651081081644, 2: 0.4054651081081644},
                                "c": {1: 0.4054651081081644, 3: 0.4054651081081644},
                                "a": {1: 1.0986122886681098},
                                "f": {3: 1.0986122886681098}}
    assert b.links_dict == {1: {2, 3}, 2: set(), 3: {1}}
    assert b.current == {1: 0.4326427188659158,
                         2: 0.23402394780075067, 3: 0.33333333333333326}


def test_index_page_rank2():
    c = index.Indexer("xml-files/PageRankExample2.xml", "txt-files/titles4.txt",
                      "txt-files/docs4.txt", "txt-files/words4.txt")
    assert c.id_title_dict == {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    assert c.relevance_dict == {'c': {1: 0.28768207245178085, 3: 0.28768207245178085, 4: 0.28768207245178085},
                                'a': {1: 0.6931471805599453, 4: 0.6931471805599453},
                                'd': {2: 0.28768207245178085, 3: 0.28768207245178085, 4: 0.28768207245178085},
                                'b': {2: 1.3862943611198906}}
    assert c.links_dict == {1: {3}, 2: {4}, 3: {4}, 4: {1, 3}}
    assert c.current == {1: 0.20184346250214996,
                         2: 0.03749999999999998,
                         3: 0.37396603749279056,
                         4: 0.3866905000050588}


def test_index_page_rank3():
    d = index.Indexer("xml-files/PageRankExample3.xml", "txt-files/titles5.txt",
                      "txt-files/docs5.txt", "txt-files/words5.txt")
    assert d.id_title_dict == {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    assert d.relevance_dict == {'f': {1: 1.3862943611198906},
                                'a': {1: 1.3862943611198906},
                                'b': {2: 1.3862943611198906},
                                'd': {3: 0.6931471805599453, 4: 0.6931471805599453},
                                'c': {3: 0.6931471805599453, 4: 0.6931471805599453}}
    assert d.links_dict == {1: set(), 2: set(), 3: {4}, 4: {3}}
    assert d.current == {1: 0.05242784862611451,
                         2: 0.05242784862611451,
                         3: 0.4475721513738852,
                         4: 0.44757215137388523}


def test_index_page_rank4():
    e = index.Indexer("xml-files/PageRankExample4.xml", "txt-files/titles6.txt",
                      "txt-files/docs6.txt", "txt-files/words6.txt")
    assert e.id_title_dict == {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    assert e.relevance_dict == {'c': {1: 0.28768207245178085, 3: 0.28768207245178085, 4: 0.28768207245178085},
                                'a': {1: 0.46209812037329684},
                                'd': {2: 0.28768207245178085, 3: 0.28768207245178085, 4: 0.14384103622589042},
                                'b': {2: 1.3862943611198906}}
    assert e.links_dict == {1: {3}, 2: {4}, 3: {4}, 4: {3}}
    assert e.current == {1: 0.0375, 2: 0.0375,
                         3: 0.46249999999999997, 4: 0.4624999999999999}


def test_metapage():
    f = index.Indexer("xml-files/test_metapage.xml", "txt-files/titles3.txt",
                      "txt-files/docs3.txt", "txt-files/words3.txt")
    assert f.id_title_dict == {1: 'first page', 2: 'Category:Computer Science'}
    assert f.relevance_dict == {'categori': {1: 0.0, 2: 0.0},
                                'comput': {1: 0.0, 2: 0.0},
                                'scienc': {1: 0.0, 2: 0.0},
                                'first': {1: 0.6931471805599453},
                                'page': {1: 0.6931471805599453},
                                'link': {2: 0.6931471805599453}}
    assert f.links_dict == {1: {2}, 2: set()}
    assert f.current == {1: 0.49999999999999994, 2: 0.49999999999999994}


def test_one_page():
    g = index.Indexer("xml-files/one_page.xml", "txt-files/titles7.txt",
                      "txt-files/docs7.txt", "txt-files/words7.txt")
    assert g.id_title_dict == {1: 'first page'}
    assert g.relevance_dict == {'page': {1: 0.0},
                                'first': {1: 0.0}}  # should this be 0?
    assert g.links_dict == {1: set()}
    assert g.current == {1: 7.59375e-05}  # is this correct?


def test_no_titles():
    h = index.Indexer("xml-files/no_titles.xml", "txt-files/titles8.txt",
                      "txt-files/docs8.txt", "txt-files/words8.txt")
    assert h.id_title_dict == {1: '', 4: ''}
    assert h.relevance_dict == {'page': {1: 0.0, 4: 0.0},
                                'titl': {1: 0.0, 4: 0.0},
                                'also': {4: 0.6931471805599453}}
    assert h.links_dict == {1: set(), 4: set()}
    assert h.current == {1: 0.49999999999999994, 4: 0.49999999999999994}


def test_no_words_or_titles():
    i = index.Indexer("xml-files/no_words_or_titles.xml", "txt-files/titles9.txt",
                      "txt-files/docs9.txt", "txt-files/words9.txt")
    assert i.id_title_dict == {1: '', 4: '', 5: ''}
    assert i.relevance_dict == {}
    assert i.links_dict == {1: set(), 4: set(), 5: set()}
    assert i.current == {1: 0.3333333333333333,
                         4: 0.3333333333333333, 5: 0.3333333333333333}


def test_no_words():
    j = index.Indexer("xml-files/no_words.xml", "txt-files/titles10.txt",
                      "txt-files/docs10.txt", "txt-files/words10.txt")
    assert j.id_title_dict == {1: 'title 1', 2: 'title 2'}
    assert j.relevance_dict == {'titl': {1: 0.0, 2: 0.0},
                                '1': {1: 0.6931471805599453},
                                '2': {2: 0.6931471805599453}}
    assert j.links_dict == {1: set(), 2: set()}
    assert j.current == {1: 0.49999999999999994, 2: 0.49999999999999994}


def test_one_word():
    k = index.Indexer("xml-files/one_word.xml", "txt-files/titles11.txt",
                      "txt-files/docs11.txt", "txt-files/words11.txt")
    assert k.id_title_dict == {1: 'title'}
    assert k.relevance_dict == {'titl': {1: 0.0}}
    assert k.links_dict == {1: set()}
    # assert k.current == {1: 1}  # ask if this should be 1?? .0000759375


def test_no_pages():
    k = index.Indexer("xml-files/no_pages.xml", "txt-files/titles11.txt",
                      "txt-files/docs11.txt", "txt-files/words11.txt")
    assert k.id_title_dict == {}
    assert k.relevance_dict == {}
    assert k.links_dict == {}
    assert k.current == {}


# def test_index_invalid_args():
#     assert index.Indexer("PageRankExample1.xml", "titles2.txt",
#                          "docs2.txt") is "Wrong number of arguments!!!"
    # how to call this??
