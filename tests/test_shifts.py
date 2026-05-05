from ..piraye.tasks.normalizer.impl.character_normalizer import NormalizationState


def test_shift1():
    # Test "ab__c_d" map to "abcd"
    state = NormalizationState()
    state.add_char("a", 0)
    state.add_char("b", 1)
    state.add_char("c", 4)
    state.add_char("", 5)
    state.add_char("d", 6)
    assert state.finalize().shifts == [(2, 2), (3, 1)]


def test_shift2():
    # Test "ab.c" map to "ab. c"
    state = NormalizationState()
    state.add_char("a", 0)
    state.add_char("b", 1)
    state.add_char(".", 2)
    state.add_char(" ", None)
    state.add_char("c", 3)
    assert state.finalize(4).shifts == [(4, -1)]


def test_shift2_2():
    # Test "ab.c" map to "ab.___c"
    state = NormalizationState()
    state.add_char("a", 0)
    state.add_char("b", 1)
    state.add_char(".___", 2)
    state.add_char("c", 3)
    assert state.finalize(4).shifts == [(6, -3)]


def test_shift3():
    # Test "a____b.c" map to "a_b._c"
    state = NormalizationState()
    state.add_char("a", 0)
    state.add_char("_", 4)
    state.add_char("b", 5)
    state.add_char(".", 6)
    state.add_char(" ", None)
    state.add_char(" ", None)
    state.add_char(" ", None)
    state.add_char("c", 7)
    assert state.finalize(8).shifts == [(1, 3), (7, -3)]


def test_shift4():
    # Test "a____b." map to "a_b._"
    state = NormalizationState()
    state.add_char("a", 0)
    state.add_char("_", 4)
    state.add_char("b", 5)
    state.add_char(".", 6)
    state.add_char(" ", None)
    assert state.finalize(7).shifts == [(1, 3), (5, -1)]


def test_shift5():
    # Test "a!b" map to "a_!_b."
    state = NormalizationState()
    state.add_char("a", 0)
    state.add_char("_", None)
    state.add_char("!", 1)
    state.add_char("_", None)
    state.add_char("b", 2)
    state.add_char(".", None)
    assert state.finalize(3).shifts == [(2, -1), (4, -1), (6, -1)]


def test_shift6():
    # Test "a!b" map to "AAAA!!!BBBBB"
    state = NormalizationState()
    state.add_char("AAAA", 0)
    state.add_char("!!!", 1)
    state.add_char("BBBBB", 2)
    assert state.finalize(3).shifts == [(4, -3), (7, -2), (12, -4)]


def test_shift7():
    # Test "a!b" map to "ABBBBB"
    state = NormalizationState()
    state.add_char("A", 0)
    state.add_char("", 1)
    state.add_char("BBBBB", 2)
    assert state.finalize(3).shifts == [(1, 1), (6, -4)]
