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

def make_add(impl):
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
            impl(click, filename, authors, title, keywords, doi)

    return add

def make_get(impl):
    @click.command()
    @click.option('--hash', type=str, help='hash of the stored file')
    def get(hash):
        """download an article"""
        if not hash:
            click.echo('Please provide a hash to look for.\nSee [COMMAND] --help for more information.')
        else:
            impl(click, hash)

    return get

def make_find(impl):
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
            impl(click, authors, title, keywords, doi)

    return find

def format_article(article_dict):
    authors = 'Authors: ' + ' ,'.join(article_dict['authors'])
    title = 'Title: ' + article_dict['title']
    keywords = 'Keywords: ' + ' ,'.join(article_dict['keywords'])
    doi = 'DOI: ' + article_dict['doi']
    link = 'Download link: ' + article_dict['link']
    return '\n'.join([authors, title, keywords, doi, link])
