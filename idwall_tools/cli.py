import click

from .strings.wrap import wrap
from .crawlers.reddit_scraper import get_high_upvotes_threads


@click.group()
def cli():
    pass


@click.command(name='textwrap')
@click.option('-j', '--justified', is_flag=True)
@click.option('-c', '--columns', default=40, type=int)
@click.argument('text')
def textwrap(text, columns, justified):
    wrapped_text = wrap(text, columns=columns, justified=justified)
    for line in wrapped_text:
        click.echo(line)


@click.command(name='scrape-reddit')
@click.argument('subreddits', type=str)
def scrape_reddit(subreddits):
    for thread in get_high_upvotes_threads(subreddits):
        print(thread)


cli.add_command(textwrap)
cli.add_command(scrape_reddit)
