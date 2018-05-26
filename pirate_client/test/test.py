from pirate_client.paper_client import PaperClient
from pirate_client.root_holder import DebugRootHolder
from pirate_client.multi_index import MultiIndex

import ipfsapi
from pathlib import Path


# one big test, because fuck it, don't have time for this shit
def test():
    api = ipfsapi.connect('127.0.0.1', 5001)
    index = MultiIndex(api, DebugRootHolder(api))
    client = PaperClient(api, index)

    test_dir = Path(__file__).parent
    files_with_meta = [
        (str(test_dir.joinpath('file1.txt')), dict(authors='me', doi='doi:/1')),
        (str(test_dir.joinpath('file2.txt')), dict(authors='myself', doi='doi:/2', keywords=['blockchain', 'consensus', 'block'])),
        (str(test_dir.joinpath('file3.txt')), dict(authors=['me', 'myself', 'again'], doi='doi:/3', keywords=['bitcoin', 'hype', 'blockchain']))
    ]
    name_id = 0
    meta_id = 1

    client.add_file(files_with_meta[0][1], files_with_meta[0][0])
    files = client.find_file(query=dict(authors='me'))
    assert len(files) >= 1
    files = client.find_file(query=dict(doi='doi:/1'))
    assert len(files) >= 1
    files = client.find_file(query=dict(doi='doi:/5'))
    assert len(files) == 0
    files = client.find_file(query=dict(authors=['myself', 'again']))

    client.add_file(files_with_meta[1][1], files_with_meta[1][0])
    files = client.find_file(query=dict(authors='me'))
    files = client.find_file(query=dict(doi='doi:/1'))
    files = client.find_file(query=dict(doi='doi:/2'))
    assert len(files) >= 1
    files = client.find_file(query=dict(keywords=['blockchain', 'block']))

    for fwm in files_with_meta:
        client.add_file(fwm[1], fwm[0])

    files = client.find_file(query=dict(authors='me'))
    files = client.find_file(query=dict(authors='myself'))
    files = client.find_file(query=dict(doi='doi:/1'))
    files = client.find_file(query=dict(doi='doi:/2'))
    files = client.find_file(query=dict(authors=['myself', 'again']))
    files = client.find_file(query=dict(keywords=['blockchain', 'block']))
    files = client.find_file(query=dict(keywords=['bitcoin', 'hype']))

    # test get finaly))
    for fwm in files_with_meta:
        file = client.find_file(query=fwm[1])[0]
        client.get_file(file['file_hash'], filename=fwm[0] + '.ponged')


if __name__ == "__main__":
    test()
