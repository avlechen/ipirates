import ipfsapi


class RootHolder(object):
    def get(self):
        pass

    def post(self, hash_path):
        pass


class DebugRootHolder(RootHolder):
    def __init__(self):
        self.hash_path = None

    def get(self):
        return self.hash_path

    def post(self, hash_path):
        print("New root {}".format(hash_path))
        self.hash_path = hash_path
