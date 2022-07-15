
from typing import Sequence
import json

from .abc import Commit
from .github import Repository


class Dataset:
    def __init__(self, path: str) -> None:
        self.path: str = path

        try:
            with open(path) as f:
                self.data = sorted([Commit(x) for x in json.load(f)], key=lambda x: x.timestamp)
        except: 
            self.data = []

    def first(self):
        return self.data[0]
    
    def last(self):
        return self.data[-1]

    def write_commit(self, cmt: Commit) -> int:
        """Write a commit into the datafile
        
        Return the index of the commit in the dataset
        """
        
        if cmt in self.data:
            return self.data.index(cmt)

        for i, c in enumerate(self.data):
            if c.timestamp > cmt.timestamp:
                self.data.insert(i, cmt)
                break
        else:
            self.data.append(cmt)
            i = len(self.data) - 1

        with open(self.path, 'w') as f:
            json.dump([x.asdict() for x in self.data], f)

        return i

    def write_commits(self, cmts: Sequence[Commit]) -> list[int]:
        """Write a sequence of commits into a datafile

        Return a sequence of indices of the corresponding commits
        """
        
        rets = []
        for cmt in cmts:
            rets.append(self.write_commit(cmt))

        return rets

    def __iter__(self):
        yield from self.data
