import re


RE_NON_WHITESPACE = re.compile(r'\S+')


def wrap(text, columns=40):
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
