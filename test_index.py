import pytest
import index

# why is this simple test not working ;(
    #I will camp at conceptual hours and get this working and
def test_exception():
    """ tests invalid input """
    invalid_Length = [0]
    with pytest.raises(ValueError):
        test = index.Indexer(invalid_Length)