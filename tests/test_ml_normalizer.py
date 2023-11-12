# testing Fibonacci number function
# pylint: skip-file
from ..piraye import NormalizerBuilder, MultiLingualNormalizerBuilder

fa_normalizer = NormalizerBuilder().alphabet_fa().alphabet_en().digit_fa().punctuation_fa() \
    .diacritic_delete().space_normal().tokenizing().remove_extra_spaces().build()
ar_normalizer = NormalizerBuilder().alphabet_ar().alphabet_en().digit_ar().punctuation_ar() \
    .diacritic_delete().space_normal().tokenizing().remove_extra_spaces().build()


def test_object():
    norm = MultiLingualNormalizerBuilder().build()
    assert norm is not None


def test_multi_lingual_normalization():
    text = "در این آیه کمی تفکر کنید.\nالَّذِينَ يُقِيمُونَ الصَّلاةَ وَيُؤْتُونَ الزَّكَاةَ"
    target = "در این آیه کمی تفکر کنید.\nالذین یقیمون الصلاة ویؤتون الزکاة"
    norm = MultiLingualNormalizerBuilder().set_normalizer('fa', fa_normalizer) \
        .set_normalizer('ar', ar_normalizer).main_normalizer_lang('fa').build()
    assert target == norm.normalize(text)

    text = "در این آیه کمی تفکر کنید: الَّذِينَ يُقِيمُونَ الصَّلاةَ وَيُؤْتُونَ الزَّكَاةَ"
    target = "در این آیه کمی تفکر کنید: الذین یقیمون الصلات ویوتون الزکات"
    norm = MultiLingualNormalizerBuilder().set_normalizer('fa', fa_normalizer) \
        .set_normalizer('ar', ar_normalizer).main_normalizer_lang('fa') \
        .sentence_level().build()
    assert target == norm.normalize(text)

    text = "در این آیه کمی تفکر کنید: الَّذِينَ يُقِيمُونَ الصَّلاةَ وَيُؤْتُونَ الزَّكَاةَ"
    target = "در این آیه کمی تفکر کنید: الذین یقیمون الصلاة ویؤتون الزکاة"
    norm = MultiLingualNormalizerBuilder().set_normalizer('fa', fa_normalizer) \
        .set_normalizer('ar', ar_normalizer).main_normalizer_lang('fa') \
        .word_level().build()
    assert target == norm.normalize(text)

    text = "در این 1 آیه کمی تفکر کنید: الَّذِينَ يُقِيمُونَ الصَّلاةَ وَيُؤْتُونَ الزَّكَاةَ"
    target = "در این ۱ آیه کمی تفکر کنید: الذین یقیمون الصلاة ویؤتون الزکاة"
    norm = MultiLingualNormalizerBuilder().set_normalizer('fa', fa_normalizer) \
        .set_normalizer('ar', ar_normalizer).main_normalizer_lang('fa').word_level().build()
    assert target == norm.normalize(text)
