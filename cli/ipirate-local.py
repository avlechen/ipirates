import json
from pathlib import Path

from cli import interface

local_path = Path(__file__).parent

api = ipfsapi.connect('127.0.0.1', 5001)
index = MultiIndex(api, SteemitRootHolder(api))
paper_client = PaperClient(api, index)

def add(click, filename, authors, title, keywords, doi):
    data = {}
    data['authors'] = authors.split(',')
    data['keywords'] = keywords.split(',')
    data['title'] = title
    data['doi'] = doi

    res = paper_client.add_file(file=filename, metadata=data, is_tmp=False)
    click.echo("Article inserted!")
    click.echo(res)

def get(click, hash):
    ipfs_prefix = 'https://ipfs.io/ipfs/'
    #res = paper_client.get_file(article_hash)
    res = ipfs_prefix + article_hash
    click.echo("Here's your article")
    click.echo(res)

def find(click, authors, title, keywords, doi):
    data = {}
    if authors:
        data['authors'] = authors.split(',')
    if title:
        data['title'] = title
    if keywords:
        data['keywords'] = keywords.split(',')
    if doi:
        data['doi'] = doi

    res = paper_client.find_file(query=data)
    click.echo("Here's what we found for your request")
    click.echo(res)


interface.cli.add_command(interface.make_add(add))
interface.cli.add_command(interface.make_get(get))
interface.cli.add_command(interface.make_find(find))

if __name__ == '__main__':
    interface.cli()
