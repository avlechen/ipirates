from pirate_client.paper_client import PaperClient
from pirate_client.root_holder import DebugRootHolder
from pirate_client.multi_index import MultiIndex

import ipfsapi
from pathlib import Path


# one big test, because fuck it, don't have time for this shit
def test():
    api = ipfsapi.connect('127.0.0.1', 5001)
    index = MultiIndex(api, DebugRootHolder())
    client = PaperClient(api, index)

    test_dir = Path(__file__).parent
    files_with_meta = [
        (str(test_dir.joinpath('file1.txt')), dict(author='me', doi='doi:/1')),
        (str(test_dir.joinpath('file2.txt')), dict(author='myself', doir='doi:/2', keywords=['blockchain', 'consensus', 'block'])),
        (str(test_dir.joinpath('file3.txt')), dict(author=['me', 'myself', 'again'], doi='doi:/3', keywords=['bitcoin', 'hype', 'blockchain']))
    ]
    name_id = 0
    meta_id = 1

    client.add_file(files_with_meta[0][1], files_with_meta[0][0])
    files = client.find_file(query=dict(author='me'))
    files = client.find_file(query=dict(doi='doi:/1'))
    files = client.find_file(query=dict(doi='doi:/2'))
    files = client.find_file(query=dict(author=['myself', 'again']))

    client.add_file(files_with_meta[1][1], files_with_meta[1][0])
    files = client.find_file(query=dict(author='me'))
    files = client.find_file(query=dict(doi='doi:/1'))
    files = client.find_file(query=dict(doi='doi:/2'))
    files = client.find_file(query=dict(keyword=['blockchain', 'block']))

    for fwm in files_with_meta:
        client.add_file(fwm[1], fwm[0])

    files = client.find_file(query=dict(author='me'))
    files = client.find_file(query=dict(author='myself'))
    files = client.find_file(query=dict(doi='doi:/1'))
    files = client.find_file(query=dict(doi='doi:/2'))
    files = client.find_file(query=dict(author=['myself', 'again']))
    files = client.find_file(query=dict(keyword=['blockchain', 'block']))
    files = client.find_file(query=dict(keyword=['bitcoin', 'hype']))

    # test get finaly))
    for fwm in files_with_meta:
        file = client.find_file(query=fwm[1])
        client.get_file(file['file_hash'], fwm[0] + '.ponged')
