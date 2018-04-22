import zlib

class Index(object):
    def __init__(self, key, api):
        self._key = key
        self._api = api


def find_index(links, key):
    for link in links:
        if link['Name'] == key:
            return link['Hash']

    return None


class Trie(Index):
    END = '<end>'

    def __init__(self, key, api):
        super().__init__(key, api)

    def make_trie(self, keys):
        root = dict()
        for key in keys:
            current_dict = root

            for letter in key:
                current_dict = current_dict.setdefault(letter, {})

            current_dict[self.END] = self.END

        return root

    def update_index(self, multihash, metadata, root_links):
        if self._key not in metadata:
            return find_index(root_links, self._key)

        root_link = find_index(root_links, self._key)

        keys = metadata[self._key] if type(metadata[self._key]) is list else [metadata[self._key], ]
        trie = self.make_trie(keys)
        return self._update(root_link, trie, multihash)

    def _update(self, link, trie, multihash):
        # can be switched to dag-objects
        index = dict() if link is None else self._api.get_json(link)
        for key in trie:
            if key == self.END:
                if 'links' not in index:
                    index['links'] = list()
                index['links'].append(multihash)
                continue

            next_link = None if key not in index else index[key]
            index[key] = self._update(next_link, trie[key], multihash)

        hash_path = self._api.add_json(index)
        self._api.pin_add(hash_path)
        return hash_path

    def search(self, query, links):
        root_link = find_index(links, self._key)
        index = self._api.get_json(root_link)

        keys = query[self._key] if type(query[self._key]) is list else [query[self._key], ]
        len_2_key_map = dict(map(lambda k: (len(k), k), keys))
        key = len_2_key_map[min(len_2_key_map.keys())]

        link = None
        for letter in key:
            if letter in index:
                link = index[letter]
                index = self._api.get_json(link)

        if root_link != link and 'links' in index:
            return list(map(lambda val: self._api.get_json(val), index['links']))
        else:
            return list()


class HashTableIndex(Index):
    def __init__(self, key, api, buckets=100000):
        super().__init__(key, api)
        self._buckets = buckets

    def get_bucket(self, value):
        if type(value) is str:
            value = value.encode()
        return str(zlib.crc32(value) % self._buckets)

    def update_index(self, multihash, metadata, root_links):
        if self._key not in metadata:
            return find_index(root_links, self._key)

        root_link = find_index(root_links, self._key)
        root_index = self._api.get_json(root_link) if root_link is not None else dict()

        keys = metadata[self._key] if type(metadata[self._key]) is list else [metadata[self._key], ]

        buckets = map(lambda k: (k, self.get_bucket(k)), keys)

        for key, bucket in buckets:
            if bucket in root_index:
                bucket_link = root_index[bucket]
                bucket_index = self._api.get_json(bucket_link)
            else:
                bucket_index = dict()

            if key not in bucket_index:
                bucket_index[key] = dict(links=list())
            elif 'links' not in bucket_index[key]:
                bucket_index[key]['links'] = list()
            bucket_index[key]['links'].append(multihash)
            bucket_link = self._api.add_json(bucket_index)

            root_index[bucket] = bucket_link

        return self._api.add_json(root_index)

    def search(self, query, links):
        root_link = find_index(links, self._key)
        root_index = self._api.get_json(root_link) if root_link is not None else dict()

        key = query[self._key] if type(query[self._key]) is not list else query[self._key][0]

        bucket = self.get_bucket(key)
        if bucket not in root_index:
            return list()

        bucket_link = root_index[bucket]
        bucket_index = self._api.get_json(bucket_link)

        links = bucket_index[key]['links']
        return list(map(lambda val: self._api.get_json(val), links))


class MultiIndex(object):
    def __init__(self, api, root_holder):
        self.root_holder = root_holder
        self.api = api
        self.indices = dict(
            author=HashTableIndex('author', api, buckets=10000),
            doi=HashTableIndex('doi', api),
            keywords=Trie('keywords', api),
        )

    def update_index(self, multihash, metadata):
        root = self.api.object_get(self.root_holder.get())

        new_links = []
        for key, index in self.indices.items():
            index_hash = index.update_index(multihash, metadata, root['Links'])
            if index_hash is not None:
                new_links.append(dict(Hash=index_hash, Name=key))

        root['Links'] = new_links
        self.root_holder.post(root)

    def search(self, query):
        links = self.api.object_get(self.root_holder.get())['Links']

        metadata_collection = []
        for key in ['doi', 'author', 'keywords']:
            if key in query:
                ret = self.indices[key].search(query, links)
                if type(ret) is list:
                    metadata_collection += ret
                else:
                    metadata_collection.append(ret)

                del query[key]
                return list(filter(lambda it: self.satisfies(it, query), metadata_collection))

    @staticmethod
    def satisfies(item, query):
        for key in query:

            def to_set(collection):
                return set(collection if type(collection) is list else [collection,])

            q = to_set(query[key])
            i = to_set(item[key])
            if not q.issubset(i):
                return False

        return True
