import json
import requests
from requests_toolbelt import MultipartEncoder
from pathlib import Path

from cli import interface

local_path = Path(__file__).parent

def add(click, filename, authors, title, keywords, doi):
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

def get(click, hash):
    res = requests.get('http://0.0.0.0:5000/article/' + hash)
    content = json.loads(res.text)
    click.echo(content['message'])
    click.echo(content['link'])

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
    res = requests.post('http://0.0.0.0:5000/article/find', json=data)
    content = json.loads(res.text)
    click.echo(content['message'])
    click.echo(content['articles'])


interface.cli.add_command(interface.make_add(add))
interface.cli.add_command(interface.make_get(get))
interface.cli.add_command(interface.make_find(find))

if __name__ == '__main__':
    interface.cli()
