import click

from .strings.wrap import wrap


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


cli.add_command(textwrap)
