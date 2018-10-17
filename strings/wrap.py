import re
import random


RE_NON_WHITESPACE = re.compile(r'\S+')


def wrap(text, columns=40, justified=False):
    """Make a generator that takes a text and yields wrapped line.

    All lines fits the width defined by :columns:.

    The text is splitted in chunks. Each chunk is a simple word
    or a word preceded or succeded by one or more special characters

    e.g. In the sentence (str): '"Let there be light,"'
         the chunks are: ['"Let', 'there', 'be', 'light,"']

    :param text: a paragraph (str)
    :param columns: delimiter of a line width (int)
    """
    cur_chunks_length = 0
    cur_line = []

    # RE_NON_WHITESPACE works like str.split(),
    # but the values are lazily-evaluated
    for match in RE_NON_WHITESPACE.finditer(text):
        chunk = match.group()
        chunk_length = len(chunk)

        if chunk_length > columns:
            raise ValueError('word or text chunk is too big to fit in '
                             f'{columns} columns: {chunk}.')

        # Number of nodes to insert whitespaces: number_of_chunks - 1
        whitespaces_nodes = len(cur_line) - 1
        if cur_chunks_length + chunk_length + whitespaces_nodes < columns:
            cur_chunks_length += chunk_length
            cur_line.append(chunk)
        else:
            _fill_with_whitespaces(cur_line, columns, justified)

            yield chunks_to_str(cur_line)

            cur_chunks_length = chunk_length
            cur_line = [chunk]

    # Remaining chunks that did not fit to complete a full line
    if cur_line:
        _fill_with_whitespaces(cur_line, columns, justified)
        yield chunks_to_str(cur_line)


def justify_line(line, columns):
    chunks_length = sum(map(len, line))
    if chunks_length > columns:
        raise ValueError('The text line length is greater than the '
                         'number of columns.')

    whitespace_nodes = len(line) - 1
    whitespaces_remaining = columns - chunks_length
    while whitespaces_remaining > 0:
        if whitespace_nodes > whitespaces_remaining:
            _add_whitespace_at_random_position(line)
            whitespaces_remaining -= 1
        elif whitespace_nodes < whitespaces_remaining:
            _add_whitespace_between_all_chunks(line)
            whitespaces_remaining -= whitespace_nodes
        else:
            _add_whitespace_between_all_chunks(line)
            whitespaces_remaining -= whitespace_nodes


def _add_whitespace_between_all_chunks(line):
    """Append a whitespace character between all pair of chunks (In-Place)

    :param line: a list of chunks (str)
    """
    for index in range(0, len(line) - 1):
        line[index] += ' '


def _add_whitespace_at_random_position(line):
    """Append a whitespace character in between a random pair of chunks (In-Place)

    :param line: a list of chunks (str)
    """
    index = random.randint(0, len(line) - 2)
    line[index] += ' '


def _fill_with_whitespaces(line, columns, justified):
    """Takes a list of strings and returns a single string
    with whitespaces between each list item

    :param line: a list of chunks (str)
    :param columns: an integer to limit the max number of
    characeters per line
    :param justified: bool
    :return: a line of text (string)
    :rtype: str
    """
    _add_whitespace_between_all_chunks(line)

    if justified:
        justify_line(line, columns)


def chunks_to_str(line):
    return ''.join(line)
