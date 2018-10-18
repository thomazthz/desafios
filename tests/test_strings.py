import pytest

from idwall_tools.strings.wrap import wrap
from idwall_tools.utils import join_newline


small_texts = [
    ('YOU SHALL NOT PASS!', 'YOU SHALL NOT PASS!'),
    ('Fly you fools!', 'Fly you fools!'),
    ('When in doubt, follow your nose.', 'When in doubt, follow your nose.'),
    ('a', 'a'),
    ('a'*39, 'a'*39),
    (' ', ''),
    ('', '')
]


def test_wrap_with_defaults(input_1, input_2, output_1, output_2):
    assert join_newline(wrap(input_1)) == output_1
    assert join_newline(wrap(input_2)) == output_2


@pytest.mark.parametrize('text_input, expected', small_texts)
def test_wrap_when_text_smaller_than_columns(text_input, expected):
    wrapped_text = join_newline(wrap(text_input))
    assert wrapped_text == expected


def test_justified_wrapped_text(input_1, input_2, output_1, output_2):
    """The justified wrapped texts can't be compared with
    the output sample given by `data/output_parte2.txt`
    since the `justify_line` function sometimes adds
    random whitespaces.
    So this function asserts only the length of each line
    and its str contents, ignoring all whitespace characters.
    """
    splitted_output = output_1.split('\n')
    justified_text = wrap(input_1, justified=True)
    for line, expected in zip(justified_text, splitted_output):
        assert len(line) == 40
        assert line.split() == expected.split()

    splitted_output = output_2.split('\n')
    justified_text = wrap(input_2, justified=True)
    for line, expected in zip(justified_text, splitted_output):
        assert len(line) == 40
        assert line.split() == expected.split()
