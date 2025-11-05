# testing Fibonacci number function
# pylint: skip-file
import pytest

from ..piraye.tasks.tokenizer.tokenizers.spacy_tokenizer import SpacyWordTokenizer
from ..piraye import NormalizerBuilder


def test_object():
    norm = NormalizerBuilder().build()
    assert norm is not None


def test_not_changing_input():
    text = "این یک متن فارسی ، English می‌باشد. این متن نباید تغییر کند.سال ۱۴۰۰ (1400)"
    norm = NormalizerBuilder().build()
    assert text == norm.normalize(text)[0]


def test_number():
    text = "1.2"
    norm = NormalizerBuilder().digit_fa().build()
    assert text != norm.normalize(text)


def test_number_tokenize():
    text = "1,200 , "
    norm = NormalizerBuilder().punctuation_fa().tokenizing().build()
    assert "1,200 ، " == norm.normalize(text)[0]


def test_add_space_after_comma():
    text = "i,am"
    norm = NormalizerBuilder().space_normal().remove_extra_spaces().alphabet_en().punctuation_en().build()
    # assert "Hello, Piraye (NLP Tool).\n" != norm.normalize(text)
    assert "i, am" == norm.normalize(text)[0]
    # text1 = "Hello  , Piraye (   NLP Tool   )  .  \n   \n"
    # norm = NormalizerBuilder().remove_extra_spaces().alphabet_en().punctuation_en().build()
    # assert "Hello , Piraye (NLP Tool ) .\n" == norm.normalize(text1)


def test_space():
    text = "Hello  ,Piraye(   NLP Tool   )  .  \n   \n"
    norm = NormalizerBuilder().space_normal().remove_extra_spaces().alphabet_en().punctuation_en().build()
    # assert "Hello, Piraye (NLP Tool).\n" != norm.normalize(text)
    assert "Hello , Piraye (NLP Tool ) .\n" == norm.normalize(text)[0]
    # text1 = "Hello  , Piraye (   NLP Tool   )  .  \n   \n"
    # norm = NormalizerBuilder().remove_extra_spaces().alphabet_en().punctuation_en().build()
    # assert "Hello , Piraye (NLP Tool ) .\n" == norm.normalize(text1)


def test_shift():
    text = "0,3  5 \t\n.9.x.y.z"
    norm = NormalizerBuilder().space_normal().remove_extra_spaces().alphabet_en().punctuation_en().build()
    text2, result = norm.normalize(text)
    shifts = result.shifts
    assert "0, 3 5\n. 9. x. y. z" == text2
    assert [(3, -1), (5, 0), (7, 2), (9, 1), (12, 0), (15, -1), (18, -2)] == shifts
    assert norm.calc_original_position(shifts, 3) == 2
    assert norm.calc_original_position(shifts, 13) == 13
    assert norm.calc_original_position(shifts, 15) == 14
    assert norm.calc_original_position(shifts, 19) == 17
    assert norm.calc_original_positions(shifts, [3, 13, 15, 19]) == [2, 13, 14, 17]
    with pytest.raises(Exception) as e:  # یا نوع خاص خطا مثل ValueError
        norm.calc_original_positions(shifts, [13, 3, 15, 19])
        assert str(e.value) == "The position list is not sorted"


def test_quotes():
    text = "«"
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    norm.normalize(text)
    text = " «««« تست "
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    norm.normalize(text)
    text = " \" تست '' تست «««« تست "
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    norm.normalize(text)


def test_quotes_spacy():
    tokenizer = SpacyWordTokenizer()
    text = "«"
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().tokenizing(tokenizer=tokenizer).build()
    assert "\"" == norm.normalize(text)[0]
    text = " «««« تست "
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    assert ' """" تست ' == norm.normalize(text)[0]
    text = " \" تست '' تست «««« تست "
    norm = NormalizerBuilder().digit_en().punctuation_en().alphabet_fa() \
        .tokenizing().remove_extra_spaces().build()
    assert ' " تست \'\' تست """" تست ' == norm.normalize(text)[0]


def test_punc_positions_basic():
    """Test basic punctuation position tracking"""
    text = "Hello, World!"
    norm = NormalizerBuilder().alphabet_en().punctuation_en().build()
    normalized_text, result = norm.normalize(text)

    # Check that punc_positions is a list
    assert isinstance(result.punc_positions, list)

    # Check expected punctuation positions
    assert len(result.punc_positions) == 2
    assert 5 in result.punc_positions  # comma position
    assert 12 in result.punc_positions  # exclamation position

    # Verify actual characters at positions
    for pos in result.punc_positions:
        char = normalized_text[pos]
        assert char in "،,!.;:?؛", f"Character at position {pos} should be punctuation, got '{char}'"


def test_punc_positions_farsi():
    """Test punctuation position tracking in Farsi text"""
    text = "سلام، این یک متن است."
    norm = NormalizerBuilder().alphabet_fa().punctuation_fa().build()
    normalized_text, result = norm.normalize(text)

    assert len(result.punc_positions) == 2

    # Check for Farsi comma and period
    comma_pos = result.punc_positions[0]
    period_pos = result.punc_positions[1]

    assert normalized_text[comma_pos] == '،'
    assert normalized_text[period_pos] == '.'


def test_punc_positions_multiple_punctuation():
    """Test tracking multiple punctuation marks"""
    text = "Hello, World! How are you? I'm fine; thanks."
    norm = NormalizerBuilder().alphabet_en().punctuation_en().remove_extra_spaces().build()
    normalized_text, result = norm.normalize(text)

    # Should find comma, exclamation, question mark, apostrophe, semicolon, period
    assert len(result.punc_positions) >= 5

    # Verify all positions contain punctuation
    for pos in result.punc_positions:
        char = normalized_text[pos]
        # Check if it's a punctuation character
        assert not char.isalnum() and not char.isspace(), \
            f"Position {pos} should be punctuation, got '{char}'"


def test_punc_positions_no_punctuation():
    """Test that empty list is returned when no punctuation"""
    text = "HelloWorld"
    norm = NormalizerBuilder().alphabet_en().build()
    normalized_text, result = norm.normalize(text)

    assert result.punc_positions == []


def test_punc_positions_only_punctuation():
    """Test text with only punctuation"""
    text = "...!!!"
    norm = NormalizerBuilder().punctuation_en().build()
    normalized_text, result = norm.normalize(text)

    # All characters should be punctuation
    assert len(result.punc_positions) == len(normalized_text)


def test_punc_positions_mixed_languages():
    """Test punctuation tracking in mixed language text"""
    text = "Hello, سلام! World؟"
    norm = (NormalizerBuilder()
            .alphabet_en()
            .alphabet_fa()
            .punctuation_en()
            .punctuation_fa()
            .build())
    normalized_text, result = norm.normalize(text)

    # Should track punctuation from both English and Farsi
    assert len(result.punc_positions) >= 3

    # Verify positions
    punc_chars = [normalized_text[pos] for pos in result.punc_positions]
    assert '،' in punc_chars or ',' in punc_chars
    assert '!' in punc_chars
    assert '؟' in punc_chars or '?' in punc_chars


def test_punc_positions_with_spaces():
    """Test punctuation position tracking with space normalization"""
    text = "Hello  ,  World  !"
    norm = (NormalizerBuilder()
            .alphabet_en()
            .punctuation_en()
            .space_normal()
            .remove_extra_spaces()
            .build())
    normalized_text, result = norm.normalize(text)

    # Should track punctuation even after space normalization
    assert len(result.punc_positions) == 2

    # Positions should be adjusted for normalized text
    for pos in result.punc_positions:
        assert normalized_text[pos] in "،,!"


def test_punc_positions_parentheses():
    """Test punctuation tracking with parentheses and brackets"""
    text = "Hello (World) [Test]"
    norm = (NormalizerBuilder()
            .alphabet_en()
            .punctuation_en()
            .remove_extra_spaces()
            .build())
    normalized_text, result = norm.normalize(text)

    # Should track parentheses and brackets
    assert len(result.punc_positions) == 4  # ( ) [ ]

    punc_chars = [normalized_text[pos] for pos in result.punc_positions]
    assert '(' in punc_chars
    assert ')' in punc_chars
    assert '[' in punc_chars
    assert ']' in punc_chars


def test_punc_positions_farsi_semicolon():
    """Test Farsi semicolon tracking"""
    text = "این است؛ آن است."
    norm = (NormalizerBuilder()
            .alphabet_fa()
            .punctuation_fa()
            .build())
    normalized_text, result = norm.normalize(text)

    assert len(result.punc_positions) == 2

    # Check for Farsi semicolon and period
    punc_chars = [normalized_text[pos] for pos in result.punc_positions]
    assert '؛' in punc_chars
    assert '.' in punc_chars


def test_punc_positions_with_digits():
    """Test punctuation tracking in text with digits"""
    text = "Price: $123.45, Total: $678.90"
    norm = (NormalizerBuilder()
            .alphabet_en()
            .digit_en()
            .punctuation_en()
            .remove_extra_spaces()
            .build())
    normalized_text, result = norm.normalize(text)

    # Should track colons, commas, and periods (but periods in numbers might be handled differently)
    assert len(result.punc_positions) >= 3

    # Verify colon and comma are tracked
    punc_chars = [normalized_text[pos] for pos in result.punc_positions]
    assert ':' in punc_chars
    assert '،' in punc_chars or ',' in punc_chars


def test_punc_positions_order():
    """Test that punctuation positions are in order"""
    text = "First, second; third. Fourth! Fifth?"
    norm = (NormalizerBuilder()
            .alphabet_en()
            .punctuation_en()
            .remove_extra_spaces()
            .build())
    normalized_text, result = norm.normalize(text)

    # Positions should be in ascending order
    assert result.punc_positions == sorted(result.punc_positions)


def test_punc_positions_with_shift():
    """Test that punctuation positions work correctly with shifts"""
    text = "0,3  5 \t\n.9.x.y.z"
    norm = (NormalizerBuilder()
            .space_normal()
            .remove_extra_spaces()
            .alphabet_en()
            .punctuation_en()
            .build())
    normalized_text, result = norm.normalize(text)

    # Should track all punctuation marks
    assert len(result.punc_positions) > 0

    # Verify that positions are valid
    for pos in result.punc_positions:
        assert 0 <= pos < len(normalized_text)
        char = normalized_text[pos]
        assert char in "،,.", f"Expected punctuation at {pos}, got '{char}'"


def test_punc_positions_empty_text():
    """Test punctuation positions with empty text"""
    text = ""
    norm = NormalizerBuilder().alphabet_en().punctuation_en().build()
    normalized_text, result = norm.normalize(text)

    assert result.punc_positions == []
    assert normalized_text == ""


def test_punc_positions_result_type():
    """Test that NormalizationResult has correct attributes"""
    text = "Test, text."
    norm = NormalizerBuilder().alphabet_en().punctuation_en().build()
    normalized_text, result = norm.normalize(text)

    # Check that result has both required attributes
    assert hasattr(result, 'shifts')
    assert hasattr(result, 'punc_positions')

    # Check types
    assert isinstance(result.shifts, list)
    assert isinstance(result.punc_positions, list)

    # Check that punc_positions contains integers
    for pos in result.punc_positions:
        assert isinstance(pos, int)
