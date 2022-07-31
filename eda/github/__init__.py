
import os
import re
from typing import Any, Sequence

from eda.github.abc import Repository


# Constants
By_GITHUB_ID = "github-id"
By_ROSTER_ID = "roster-id"


class Student(Repository):
    def __init__(self, _autoverify: bool = False, **kw) -> None:
        self.kw = kw

        super().__init__(
            *re.match(r"^https://github\.com/([\w\d]+)/([\w\d\-]+).*$",
                      kw["student_repository_url"]).groups(),
            _autoverify=_autoverify
        )


class Assignment:
    def verifyall(self):
        """Verify all student repositories"""

        for v in self._students.values():
            v.verify()

    def __init__(self, title: str, url: str, students: Sequence[dict[str, Any]], starter_code_url: str = None, _autoverify: bool = False) -> None:
        self._title: str = title
        self._url: str = url
        self._starter_code_url: str = starter_code_url

        self._students = {x["github_username"]: Student(
            **x, _autoverify=_autoverify) for x in students}

    @classmethod
    def from_roster(cls, filepath: str, **kw):
        import csv

        with open(filepath) as f:
            dt = list(csv.DictReader(f))

        return cls(
            title=dt[0].get("assignment_name"),
            url=dt[0].get("assignment_url"),
            starter_code_url=dt[0].get("starter_code_url"),
            students=dt,
            **kw
        )

    def get_students(self, by: str, key: str) -> Sequence[Student]:
        if by == By_GITHUB_ID:
            return [self._students.get(key)] if key in self._students else []

        elif by == By_ROSTER_ID:
            return [
                v for x, v in self._students.items() if key in v.kw["roster_identifier"]
            ]

        else:
            raise KeyError("invalid `by`")
