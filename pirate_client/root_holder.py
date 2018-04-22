import ipfsapi
import json
from io import BytesIO


class RootHolder(object):
    def get(self, api):
        pass

    def post(self, hash_path):
        pass

    def create_empty(self):
        root_object = dict(
            Data="{'version':0.0.0}"
        )

        return self.update_root(root_object)

    def update_root(self, root):
        root_hash = self.api.object_put(
            BytesIO(json.dumps(root).encode())
        )
        self.api.pin_add(root_hash['Hash'])
        return root_hash['Hash']


class DebugRootHolder(RootHolder):
    def __init__(self, api):
        self.hash_path = None
        self.api = api

    def get(self):
        if self.hash_path is None:
            self.hash_path = self.create_empty()

        return self.hash_path

    def post(self, root):
        print("New root {}".format(self.hash_path))
        self.hash_path = self.update_root(root)
