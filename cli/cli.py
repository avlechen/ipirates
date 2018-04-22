#!/usr/local/bin/python3

import click
import sys
import json
import requests

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
@click.option('--tags', type=str, help='list of tags as CSV string')
@click.option('--file', type=str, help='article file')
def add(authors, title, tags, file):
    """upload an article"""
    if not file:
        click.echo('Please provide file location to upload.\nSee [COMMAND --help] for more information')
    elif not authors or not title or not tags:
        click.echo('Please provide all the necessary metadate.\nSee "[COMMAND] --help" for more inforemtion.')
    else:
        data = {}
        data['authors'] = authors.split(',')
        data['tags'] = tags.split(',')
        data['title'] = title
        click.echo(data)

@click.command()
@click.option('--hash', type=str, help='hash of the stored file')
def get(hash):
    """download an article"""
    if not hash:
        click.echo('Please provide a hash to look for.\nSee [COMMAND] --help for more information.')
    else:
        click.echo(hash)

@click.command()
@click.option('--authors', type=str, help='authors name list as CSV string')
@click.option('--title', type=str, help='title of an article')
@click.option('--tags', type=str, help='list of tags as CSV string')
def find(authors, title, tags):
    """find an article"""
    if not authors and not title and not tags:
        click.echo('Please provide any search information.\nSee "[COMMAND] --help" for more information.')
    else:
        data = {}
        if authors:
            data['authors'] = authors.split(',')
        if title:
            data['title'] = title
        if tags:
            data['tags'] = tags.split(',')
        click.echo(data)

cli.add_command(add)
cli.add_command(get)
cli.add_command(find)

if __name__ == '__main__':
    cli()
