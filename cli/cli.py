import click
import sys
import json
import requests
from requests_toolbelt import MultipartEncoder
from pathlib import Path

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

local_path = Path(__file__).parent

@click.command()
@click.option('--authors', type=str, help='authors name list as CSV string')
@click.option('--title', type=str, help='title of an article')
@click.option('--keywords', type=str, help='list of keywords as CSV string')
@click.option('--doi', type=str, help='DOI - Digital Object Identifier')
@click.option('--local/--no-local', default=False)
@click.argument('filename', type=click.Path(exists=True))
def add(filename, authors, title, keywords, doi, local):
    """upload an article"""
    if not authors or not title or not keywords or not doi:
        click.echo('Please provide all the necessary metadate.\nSee "[COMMAND] --help" for more inforemtion.')
    else:
        if local:
            pass
        else:
            data = {}
            data['authors'] = authors.split(',')
            data['keywords'] = keywords.split(',')
            data['title'] = title
            data['doi'] = doi
            filepath = local_path.joinpath(filename)
            body = MultipartEncoder(
                fields={
                    'metadata': str(data).replace("'", "\""),
                    'file': (filepath.stem, filepath.open(mode='rb'))
                }
            )
            res = requests.post('http://0.0.0.0:5000/article', data=body, headers={'Content-Type': body.content_type})
            content = json.loads(res.text)
            click.echo(content['message'])
            click.echo(content['article'])

@click.command()
@click.option('--hash', type=str, help='hash of the stored file')
@click.option('--local/--no-local', default=False)
def get(hash, local):
    """download an article"""
    if not hash:
        click.echo('Please provide a hash to look for.\nSee [COMMAND] --help for more information.')
    else:
        if local:
            pass
        else:
            res = requests.get('http://0.0.0.0:5000/article/' + hash)
            content = json.loads(res.text)
            click.echo(content['message'])
            click.echo(content['link'])

@click.command()
@click.option('--authors', type=str, help='authors name list as CSV string')
@click.option('--title', type=str, help='title of an article')
@click.option('--keywords', type=str, help='list of keywords as CSV string')
@click.option('--doi', type=str, help='DOI - Digital Object Identifier')
@click.option('--local/--no-local', default=False)
def find(authors, title, keywords, doi, local):
    """find an article"""
    if not authors and not title and not keywords and not doi:
        click.echo('Please provide any search information.\nSee "[COMMAND] --help" for more information.')
    else:
        if local:
            pass
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
            res = requests.post('http://0.0.0.0:5000/article/find', json=data)
            content = json.loads(res.text)
            click.echo(content['message'])
            click.echo(content['articles'])

def format_article(article_dict):
    authors = 'Authors: ' + ' ,'.join(article_dict['authors'])
    title = 'Title: ' + article_dict['title']
    keywords = 'Keywords: ' + ' ,'.join(article_dict['keywords'])
    doi = 'DOI: ' + article_dict['doi']
    link = 'Download link: ' + article_dict['link']
    return '\n'.join([authors, title, keywords, doi, link])


cli.add_command(add)
cli.add_command(get)
cli.add_command(find)

if __name__ == '__main__':
    cli()
