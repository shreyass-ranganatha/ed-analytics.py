ed-analytics.py
===============

`ed_analytics/abc.py`
=====================

1. `class Commit` inherits `dict`

    *attributes*
    - `sha: str`
    - `**kw`

<br>

2. `class Submission`

    *attributes*
    - `assignment_name: str`
    - `assignmentURL: str`
    - `reponame: str`

        **@property**
    - `apiURL: str`
    - `httpURL: str`

    *methods*
    - `get_commits(author=None, since=None, per_page=None, page=None, until=None) -> List[Commit]`

        GitHub REST API request to fetch commits and return them

        **parameters**
        - `author: str`

            query parameter of commit author

        - `since: str`

            since timestamp in ISO 8601 format `YYYY-MM-DDTHH:MM:SSZ`

        - `per_page: int`

            query parameter for number of requests per page

        - `page: int`

            query parameter for the nth page

        - `until: str`

            until timestamp in ISO 8601 format `YYYY-MM-DDTHH:MM:SSZ`

    - `get_commit(sha) -> Commit`

        GitHub REST API request to fetch specific commit

        **parameters**
        - `sha: str`

            path parameter to commit SHA


---

## `ed_analytics/analysis.py`
1. `class ClassroomAssignment`

    *Constructors*
    - `from_assignment_grades(path: str) -> ClassroomAssignment`

        `path` is path to Assignment Grades CSV file

    *attributes*
    - `submissions: Dict[str, Submission]`

        A dictionary with *github_username* as key and the person's individual Submission as value

    *methods*

---

## References
- https://iscinumpy.gitlab.io/post/factory-classmethods-in-python/
