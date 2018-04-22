from steemit.steemit import get_last_hash_comment, send_new_hash_comment

import json
from io import BytesIO


class RootHolder(object):
    def __init__(self, api):
        self.api = api

    def get(self):
        pass

    def post(self, root):
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


class SteemitRootHolder(RootHolder):
    def __init__(self, api):
        self.root_hash = None
        super().__init__(api)

    def get(self):
        self.root_hash = get_last_hash_comment()
        if self.root_hash is None:
            self.root_hash = self.create_empty()
        else:
            self.api.pin_add(self.root_hash)

        return self.root_hash

    def post(self, root):
        new_hash = self.update_root(root)
        send_new_hash_comment(new_hash, prev_hash=self.root_hash)
        self.root_hash = new_hash


class DebugRootHolder(RootHolder):
    def __init__(self, api):
        self.hash_path = None
        super().__init__(api)

    def get(self):
        if self.hash_path is None:
            self.hash_path = self.create_empty()

        return self.hash_path

    def post(self, root):
        print("New root {}".format(self.hash_path))
        self.hash_path = self.update_root(root)
