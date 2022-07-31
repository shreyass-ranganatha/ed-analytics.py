import typing
import warnings
import re

import requests as rq

from eda.github.exceptions import RateLimitError


class Repository:
    def verify(self) -> bool:
        """Verifies the existence of the repository on https://github.com"""

        if rq.get(
            "https://api.github.com/repos/{}/{}".format(
                self.owner, self.reponame),
            headers={
                "Authorization": "token {}".format(
                    self.__oauth_token) if self.__oauth_token else None,
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "ed-analytics.py"
            }
        ).status_code != 200:
            return False
        return True

    def __init__(self, owner: str, reponame: str, _autoverify: bool = False) -> None:
        self.owner: str = owner
        self.reponame: str = reponame

        self.__oauth_token: str = None

        if _autoverify and not self.verify():
            warnings.warn("repository {} not found".format(str(self)))

    @classmethod
    def from_url(cls, url: str, **kw):
        return cls(*re.match(r"^https://github\.com/([\w\d]+)/([\w\d\-]+).*$", url).groups(), **kw)

    def authorise(self, oauth_token):
        """Authorise with GitHub oAuth token"""

        self.__oauth_token: str = oauth_token

    @property
    def url(self):
        return "https://github.com/{}/{}".format(
            self.owner, self.reponame)

    def __str__(self):
        return "{}/{}".format(
            self.owner, self.reponame)

    def get_commit(self, sha: str = None):
        """
        Parameters
        ----------
        sha : str
            SHA value of the commit

        References
        ----------
        https://docs.github.com/en/rest/commits/commits#list-commits--parameters
        """

        res = rq.get(
            "https://api.github.com/repos/{}/{}/commits/{}".format(
                self.owner, self.reponame, sha),
            headers={
                "Authorization": "token {}".format(
                    self.__oauth_token) if self.__oauth_token else None,
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "ed-analytics.py"
            }
        )

        if not (json_data := res.json()):
                return

        if res.status_code != 200:
            raise RateLimitError(json_data.get("message", "response code != 200"))

        yield json_data


    def get_commits(self, author: str = None, since: str = None, per_page: int = None, page: int = None, until: str = None) -> typing.Sequence[dict]:
        """
        Parameters
        ----------
        author : str
            query parameter of commit author

        since : str
            since timestamp in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ

        per_page : int
            number of responses per page

        page : int
            page of output

        until : str
            until timestamp in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ

        References
        ----------
        https://docs.github.com/en/rest/commits/commits#list-commits--parameters
        """

        params = {
            "author": author,
            "since": since,
            "per_page": per_page,
            "until": until
        }

        for i in range(*(
            (1, 10 + 1) if page is None
            else (page, page + 1)
        )):
            params["page"] = i

            res = rq.get(
                "https://api.github.com/repos/{}/{}/commits".format(
                    self.owner, self.reponame),
                params=params,
                headers={
                    "Authorization": "token {}".format(
                        self.__oauth_token) if self.__oauth_token else None,
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "ed-analytics.py"
                }
            )

            if not (json_data := res.json()):
                return

            if res.status_code != 200:
                raise RateLimitError(json_data.get("message", "response code != 200"))

            yield json_data
