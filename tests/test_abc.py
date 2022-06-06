from context import pytest
import datetime
import json

from ed_analytics.abc import Commit


# setup
with open("tests/files/github_commits.json") as file:
    commits_data = json.load(file)


class_commit_attributes = {
    "sha": str,
    "timestamp": datetime.datetime,
    "author": dict,
    "author_github_username": str,
    "htmlURL": str
}


class TestCommit:
    def test_object_attributes(self):
        cmt = Commit(commits_data[0])

        assert not isinstance(cmt, dict), "Shouldn't inherit from `dict`"

        for attr, kind in class_commit_attributes.items():
            assert hasattr(cmt, attr), "No attribute `{}` found".format(attr)

            assert isinstance(getattr(cmt, attr), kind) or getattr(
                cmt, attr) is None, "Expect type {} for attribute `{}`".format(kind, attr)

        attrs = [
            ar for ar in dir(cmt)
            if (ar not in class_commit_attributes) and not ar.startswith("__")
        ]
