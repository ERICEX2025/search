import pytest
import index

# why is this simple test not working ;(
# I will camp at conceptual hours and get this working and


def test_exception():
    """ tests invalid input """
    invalid_Length = [0]
    with pytest.raises(ValueError):
        test = index.Indexer(invalid_Length)


# have a case when relevance is the same?
def test_index():
    a = index.Indexer("test_tf_idf.xml", "titles.txt", "docs.txt", "words.txt")
    assert a.word_corpus is ...
