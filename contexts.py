#!/usr/bin/python3

from types import *

def judgement_ctx(context):
    """returns true if its argument is a valid context"""
    try:
        for t in context.entries.values():
            if not judgement_type(t):
                return False
        return True
    except AttributeError:
        print("something is wonky with your context-dict")
        return False


class Context():
    # uses a dict to map names to types
    tag = "{}"

    def __init__(self, entries, subset=None):
        self.entries = dict()

        if subset:
            if not judgement_ctx(subset):
                raise TypeError("'subset' is not a valid context")
            for (name, name_type) in subset:
                self.entries[name] = name_type

        for (name, name_type) in entries.items():
            if not judgement_type(name_type):
                raise TypeError(f"name_type '{name_type}' is not a valid type")
            if name in self.entries:
                raise ValueError(f"name {name} is already in use")
            self.entries[name] = name_type

    def __contains__(self, name):
        return name in self.entries.keys()

    def __iter__(self):
        for name, name_type in self.entries.items():
            yield name, name_type

    def __repr__(self):
        return f"context of {self.entries}"

    def get(self, elem):
        return self.entries.get(elem)
