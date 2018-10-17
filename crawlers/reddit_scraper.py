import re
from collections import namedtuple

from requests_html import HTMLSession


Thread = namedtuple('Thread', 'title upvotes subreddit comments_url url')

UPVOTES_THRESHOLD = 5000

session = HTMLSession()


def get_high_upvotes_threads(subreddits):
    base_url = 'https://old.reddit.com'

    if isinstance(subreddits, str):
        subreddits = subreddits.split(';')

    def gen_threads(subreddits):
        urls = [f'{base_url}/r/{subreddit.strip()}' for subreddit in subreddits]

        for url in urls:
            r = session.get(url)

            if r.status_code != 200 or not r.content:
                continue

            thread_list = r.html.find('#siteTable .thing')

            for t in thread_list:
                upvotes = t.attrs.get('data-score', '')
                try:
                    upvotes = int(upvotes)
                except ValueError:
                    continue

                subreddit = t.attrs.get('data-subreddit', url.rstrip('/').rsplit('/', 1)[-1])
                thread_url = t.attrs.get('data-url', '')
                comments_url = t.attrs.get('data-permalink', '')
                title = t.find('.title .title', first=True).text

                yield Thread(
                    title=title,
                    upvotes=upvotes,
                    subreddit=subreddit,
                    url=thread_url,
                    comments_url=f'{base_url}{comments_url}',
                )

    yield from filter(lambda t: t.upvotes >= UPVOTES_THRESHOLD, gen_threads(subreddits))
