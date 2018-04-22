import click
import os
import sys
import json
import requests
from requests_toolbelt import MultipartEncoder

from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format

init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected

#this thins prints ascii-art-style header only in case of root '--help'
if (len(sys.argv) == 1 or sys.argv[1] == '--help'):
    cprint(figlet_format('ipirates', font='jazmine'))

@click.group()
def cli():
    """get expensive academic articles for free"""
    pass

@click.command()
@click.option('--authors', type=str, help='authors name list as CSV string')
@click.option('--title', type=str, help='title of an article')
@click.option('--keywords', type=str, help='list of keywords as CSV string')
@click.option('--doi', type=str, help='DOI - Digital Object Identifier')
@click.argument('filename', type=click.Path(exists=True))
def add(filename, authors, title, keywords, doi):
    """upload an article"""
    if not authors or not title or not keywords or not doi:
        click.echo('Please provide all the necessary metadate.\nSee "[COMMAND] --help" for more inforemtion.')
    else:
        data = {}
        data['authors'] = authors.split(',')
        data['keywords'] = keywords.split(',')
        data['title'] = title
        data['doi'] = doi
        click.echo(data)
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        click.echo(filepath)
        body = MultipartEncoder(
            fields={
                'metadata': str(data).replace("'", "\""),
                'file': (filename, open(filepath, 'rb'))
            }
        )
        res = requests.post('http://0.0.0.0:5000/article', data=body)

@click.command()
@click.option('--hash', type=str, help='hash of the stored file')
def get(hash):
    """download an article"""
    if not hash:
        click.echo('Please provide a hash to look for.\nSee [COMMAND] --help for more information.')
    else:
        click.echo(hash)
        res = requests.get(f'http://0.0.0.0:5000/article/{hash}')
        click.echo(res.content)

@click.command()
@click.option('--authors', type=str, help='authors name list as CSV string')
@click.option('--title', type=str, help='title of an article')
@click.option('--keywords', type=str, help='list of keywords as CSV string')
@click.option('--doi', type=str, help='DOI - Digital Object Identifier')
def find(authors, title, keywords, doi):
    """find an article"""
    if not authors and not title and not keywords and not doi:
        click.echo('Please provide any search information.\nSee "[COMMAND] --help" for more information.')
    else:
        data = {}
        if authors:
            data['authors'] = authors.split(',')
        if title:
            data['title'] = title
        if keywords:
            data['keywords'] = keywords.split(',')
        if doi:
            data['doi'] = doi
        click.echo(data)
        requests.post('http://0.0.0.0:5000/article/find', json=data)

cli.add_command(add)
cli.add_command(get)
cli.add_command(find)

if __name__ == '__main__':
    cli()
