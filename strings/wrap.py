import re


RE_NON_WHITESPACE = re.compile(r'\S+')


def wrap(text, columns=40):
    """Make a generator that takes a text and yields wrapped line.

    All lines fits the width defined by :columns:.

    The text is splitted in chunks. Each chunk is a simple word
    or a word preceded or succeded by one or more special characters

    e.g. In the sentence (str): '"Let there be light,"'
         the chunks are: ['"Let', 'there', 'be', 'light,"']

    :param text: a paragraph (str)
    :param columns: delimiter of a line width (int)
    """
    cur_chunk_length = 0
    cur_line = []

    # RE_NON_WHITESPACE works like str.split(),
    # but the values are lazily-evaluated
    for match in RE_NON_WHITESPACE.finditer(text):
        chunk = match.group()
        # Number of nodes to insert whitespaces: number_of_chunks - 1
        whitespaces_nodes = len(cur_line) - 1
        if cur_chunk_length + len(chunk) + whitespaces_nodes < columns:
            cur_chunk_length += len(chunk)
            cur_line.append(chunk)
        else:
            yield ' '.join(cur_line)
            cur_chunk_length = 0
            cur_line = []

    # Remaining chunks that did not fit to complete a full line
    if cur_line:
        yield ' '.join(cur_line)
