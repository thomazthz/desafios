from operator import attrgetter


def pprint_thread(thread):
    extra_padding = 8
    values = attrgetter(*thread._fields)(thread)

    thread_data = []
    l_columns = 0
    for k, v in zip(thread._fields, values):
        l_columns = max([len(k), l_columns])
        thread_data.append((k.upper(), v))

    l_columns += extra_padding

    print()
    for line in thread_data:
        # print('-' * (l_columns + 1 + len(str(line[1]))))
        print(f'{line[0]:{l_columns}} {line[1]}')
        # print('-' * (l_columns + 1 + len(str(line[1]))))
    print()


def join_newline(it):
    return '\n'.join(it)
