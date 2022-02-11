# testing Fibonacci number function
# pylint: skip-file

from normalizer import Normalizer


def test_object():
    norm = Normalizer(['alphabet_fa'])
    assert norm is not None
