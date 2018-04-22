import ipfsapi
from pathlib import Path

from .multi_index import MultiIndex
from .root_holder import RootHolder
from .root_holder import DebugRootHolder


class PaperClient(object):
    def __init__(self, api=None, index=None):
        self._api = api or ipfsapi.connect('127.0.0.1', 5001)

        self.index = index or MultiIndex(api, DebugRootHolder(api))

    def get_file(self, multihash, filename=None):
        filename = filename or 'tmp/tmp{}'.format(multihash)
        path = Path(filename)
        path.parent.mkdir(exist_ok=True, parents=True)

        return self._api.get(multihash, filepath=filename)

    def add_file(self, metadata, file, is_tmp=False):
        result = self._api.add(file)

        if 'file_hash' in metadata:
            # file already in db
            if is_tmp:
                Path(file).unlink()
            return

        metadata['file_hash'] = result['Hash']
        meta_hash = self._api.add_json(metadata)
        # add magnet link?

        self.index.update_index(meta_hash, metadata)

        if is_tmp:
            Path(file).unlink()

        return metadata

    def find_file(self, query):
        metadatas = self.index.search(query)
        for metadata in metadatas:
            metadata['ipfs-url'] = 'http://gateway.ipfs.io/ipfs/{}'.format(metadata['file_hash'])
        return metadatas
