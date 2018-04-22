import zlib
import json


class Index(object):
    def __init__(self, key, api):
        self.key = key
        self.api = api


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
        root_link = root_links[self.key]

        keys = metadata[self.key] if type(metadata[self.key]) is list else [metadata[self.key], ]
        trie = self.make_trie(keys)
        return self._update(root_link, trie, multihash)

    def _update(self, link, trie, multihash):
        # can be switched to dag-objects
        index = dict() if link is None else json.loads(self.api.cat(link))
        for key in trie:
            if key == self.END:
                index['links'].append(multihash)
            next_link = None if key not in index else index[key]
            index[key] = self._update(next_link, trie[key], multihash)

        return self.api.add_json(index)

    def search(self, query, links):
        root_link = links[self.key]
        index = json.loads(self.api.cat(root_link))

        keys = query[self.key] if type(query[self.key]) is list else [query[self.key], ]
        len_2_key_map = dict(map(lambda k: (len(k), k), keys))
        key = len_2_key_map[min(len_2_key_map.keys())]

        link = None
        for letter in key:
            if letter in index:
                link = index[letter]
                index = json.loads(self.api.cat(link))

        if root_link != link:
            return index['links'] if 'links' in index else []


class HashTableIndex(Index):
    def __init__(self, key, api, buckets=100000):
        super().__init__(key, api)
        self.buckets = buckets

    def get_bucket(self, value):
        return zlib.crc32(value) % self.buckets

    def update_index(self, multihash, metadata, root_links):
        root_link = root_links[self.key]
        root_index = json.loads(self.api.cat(root_link))

        keys = metadata[self.key] if type(metadata[self.key]) is list else [metadata[self.key], ]

        buckets = map(self.get_bucket, keys)

        for bucket in buckets:
            if bucket in root_index:
                bucket_link = root_index[bucket]
                bucket_index = json.loads(self.api.cat(bucket_link))
            else:
                bucket_index = dict()

            bucket_index[metadata[self.key]] = multihash
            bucket_link = self.api.add_json(bucket_index)

            root_index[bucket] = bucket_link

        return self.api.add_json(root_index)

    def search(self, query, links):
        root_link = links[self.key]
        root_index = json.loads(self.api.cat(root_link))

        key = query[self.key] if type(query[self.key]) is not list else query[self.key][0]

        bucket = self.get_bucket(key)
        bucket_link = root_index[bucket]
        bucket_index = json.loads(self.api.cat(bucket_link))

        return list(bucket_index.values)


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

        root['Links'] = []
        for key, index in self.indices.items():
            root['Links'].append(dict(
                Hash=index.update_index(multihash, metadata, root['Links']),
                Name=key
            ))

        root_multihash = self.api.object_put()
        self.root_holder.put(root_multihash)

    def search(self, query):
        links = self.api.object_get(self.root_holder.get())['Links']

        selection = []
        search_priority = ['doi', 'author', 'keyword']
        for key in search_priority:
            if key in query:
                selection = self.indices[key].search(query, links)
            del query[key]

        return filter(lambda it: self.satisfies(it, query), selection)

    @staticmethod
    def satisfies(item, query):
        unpacked = json.loads(item)
        for key in query:
            if query[key] not in unpacked[key]:
                return False

        return True
