
class setmap(object):

    def __init__(self):
        self.data = {}

    def add(self, key, value):
        if key not in self.data:
            self.data[key] = set()
        self.data[key].add(value)

    def get(self, key):
        return [x for x in self.data[key]]

    def count(self, key):
        return len(self.data[key])

    def max_count(self):
        return len(max(self.data.values(), key=len))

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
