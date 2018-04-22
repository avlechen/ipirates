import ipfsapi
from pathlib import Path

from .multi_index import MultiIndex
from .root_holder import RootHolder


class PaperClient(object):
    def __init__(self, api=None, index=None):
        self.api = api or ipfsapi.connect('127.0.0.1', 5001)

        self.index = index or MultiIndex(api, DebugRootHolder)

    def get_file(self, multihash, filename=None):
        filename = filename or 'tmp/tmp{}'.format(multihash)
        path = Path(filename)
        path.parent.mkdir(exist_ok=True, parents=True)

        return self.api.cat(multihash, filepath='tmp.')

    def add_file(self, metadata, file):
        result = self.api.add(file)

        assert 'file_hash' not in metadata
        metadata['file_hash'] = result['Hash']
        meta_hash = self.api.add_json(metadata)
        # add magnet link?

        self.index.update_index(meta_hash, metadata)

        path = Path(file)
        path.unlink()

    def find_file(self, query):
        metadata = self.index.search(query)
        metadata['ipfs-url'] = 'http://gateway.ipfs.io/ipfs/{}'.format(metadata['file_hash'])
        return metadata
