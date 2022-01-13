import re
import json
import time
import pymongo
import logging
import pathlib
import traceback
import dateutil.parser
import pandas as pd
import multiprocessing as mp

from typing import *
from datetime import datetime, timedelta
from github import Github
from github.Repository import Repository
from github.Issue import Issue
from github.IssueEvent import IssueEvent
from github.NamedUser import NamedUser
from github.PaginatedList import PaginatedList
from github.GithubException import RateLimitExceededException, UnknownObjectException

T = TypeVar("T")
with open("config.json", "r") as f:
    CONFIG = json.load(f)
MONGO_URL = CONFIG["mongodb"]
TOKENS = CONFIG["tokens"]


def page_num(per_page: int, total_count: int) -> int:
    """Calculate total number of pages given page size and total number of items"""
    assert per_page > 0 and total_count >= 0
    if total_count % per_page == 0:
        return total_count // per_page
    return total_count // per_page + 1


def test_page_num():
    assert page_num(30, 90) == 3
    assert page_num(30, 91) == 4


def match_issue_numbers(text: str) -> List[int]:
    """
    Match close issue text in a pull request, as documented in:
    https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
    """
    numbers = []
    regex = r"(close[sd]?|fix(es|ed)?|resolve[sd]?) \#(\d+)"
    for _, _, number in re.findall(regex, text.lower()):
        numbers.append(int(number))
    return numbers


def test_match_issue_numbers():
    assert match_issue_numbers("abc") == []
    assert match_issue_numbers("close #db") == []
    assert match_issue_numbers("close #1 closes #2 closed #3") == [1, 2, 3]
    assert match_issue_numbers("fix #3 fiXes #2 fixed #1") == [3, 2, 1]
    assert match_issue_numbers("Resolve #2 resolves #1 resolved #3") == [2, 1, 3]


def request_github(
    gh: Github, gh_func: Callable[[], T], default: Any = None
) -> Optional[T]:
    """
    This is a wrapper to ensure that any rate-consuming interactions with GitHub
      have proper exception handling.
    """
    for _ in range(0, 3):  # Max retry 3 times
        try:
            data = gh_func()
            return data
        except RateLimitExceededException as ex:
            logging.info("{}: {}".format(type(ex), ex))
            sleep_time = gh.rate_limiting_resettime - time.time() + 10
            logging.info(
                "Rate limit reached, wait for {} seconds...".format(sleep_time)
            )
            time.sleep(max(1.0, sleep_time))
        except UnknownObjectException as ex:
            logging.error("{}: {}".format(type(ex), ex))
            break
        except Exception as ex:
            logging.error("{}: {}".format(type(ex), ex))
            time.sleep(5)
    return default


def estimate_historical_issues(gh: Github, repo: Repository) -> List[dict]:
    """
    Estimate historical issue statistics using pre-cached data
    Ideally, it should be computed based on latest data on GitHub,
      but it costs too many queries, so an alternative is to use the data
      we crawled from MongoDB as an estimation
    """
    global MONGO_URL
    db = pymongo.MongoClient(MONGO_URL).gfi_rec
    issues = list(db.issues.find({"owner": repo.owner.login, "name": repo.name}))

    # Scan merged PRs to get what issues they close, if any
    issue_num_to_close_pull: Dict[int, int] = dict()
    for issue in issues:
        if issue["pull"] is None or not issue["pull"]["merged"]:
            continue
        for text in [issue["pull"]["title"], issue["pull"]["body"]] + [
            c["body"] for c in issue["comments"]
        ]:
            if text is None:
                continue
            for num in match_issue_numbers(text):
                issue_num_to_close_pull[num] = issue

    # for all issues, get its open time, closed time, # of closers' commits at close time
    logging.info(f"{len(issues)} issues to collect statistics")
    issue_stats = []
    for issue in issues:
        if issue["pull"] is not None or issue["issue"]["state"] != "closed":
            continue
        issue_stat = {
            "number": issue["number"],
            "created_at": issue["issue"]["created_at"],
            "closed_at": issue["issue"]["closed_at"],
            "closer_commit_num": None,
        }
        close_time = dateutil.parser.parse(issue["issue"]["closed_at"])
        close_events = [e for e in issue["events"] if e["event"] == "closed"]
        if issue["number"] in issue_num_to_close_pull:
            pull = issue_num_to_close_pull[issue["number"]]
            user = pull["pull"]["user"]["login"]
            issue_stat["closer_commit_num"] = request_github(
                gh, lambda: repo.get_commits(author=user, until=close_time).totalCount
            )
        else:
            for event in close_events:
                if event["commit_id"] is not None:
                    author = request_github(
                        gh, lambda: repo.get_commit(sha=event["commit_id"]).author
                    )
                    issue_stat["closer_commit_num"] = request_github(
                        gh,
                        lambda: repo.get_commits(
                            author=author, until=close_time
                        ).totalCount,
                    )
        issue_stats.append(issue_stat)

    return issue_stats


def get_closer_commits(gh: Github, issue: Issue) -> Optional[int]:
    """ 
    Given an Issue, if it is already closed, 
      we use various heuristics to find commit or PR that closed it,
      and compute in this repo the number of commits by the closer at close time.
    """
    assert request_github(
        gh, lambda: issue.state == "closed" and "pull_request" not in issue.raw_data
    )
    repo = request_github(gh, lambda: issue.repository)
    repo_name = request_github(gh, lambda: repo.owner.login + "/" + repo.name)

    # Find a PR first, if any
    t1 = issue.closed_at - timedelta(minutes=1)
    t2 = issue.closed_at + timedelta(minutes=1)
    query = f"repo:{repo_name} is:pr merged:{t1.isoformat()}..{t2.isoformat()}"
    pulls = request_github(gh, lambda: list(gh.search_issues(query)), [])
    for pull in pulls:
        comments = request_github(gh, lambda: [c.body for c in pull.get_comments()], [])
        for text in [pull.title, pull.body] + comments:
            if text is None:
                continue
            for num in match_issue_numbers(text):
                if num == issue.number:
                    logging.info(
                        f"{repo_name} issue {issue.number} closed by {pull.url}"
                    )
                    return request_github(
                        gh,
                        lambda: repo.get_commits(
                            author=pull.user, until=issue.closed_at
                        ).totalCount,
                    )

    # If we cannot find a corresponding pull request,
    #   resort to finding related commits
    close_events: List[IssueEvent] = [
        e
        for e in request_github(gh, lambda: list(issue.get_events()), [])
        if e.event == "closed"
    ]
    for event in close_events:
        if event.commit_id is not None:
            logging.info(
                f"{repo_name} issue {issue.number} closed by {event.commit_id}"
            )
            author = request_github(
                gh, lambda: repo.get_commit(sha=event.commit_id).author
            )
            return request_github(
                gh,
                lambda: repo.get_commits(
                    author=author, until=issue.closed_at
                ).totalCount,
            )
    return None


def test_get_closer_commits():
    """
    Some example issues closed by PR: 
        https://github.com/osmlab/name-suggestion-index/issues/4957
        https://github.com/HabitRPG/habitica/issues/12276
        https://github.com/HabitRPG/habitica/issues/12698
    An example issue closed by commit: https://github.com/osmlab/name-suggestion-index/issues/1881
    """
    global TOKENS
    gh = Github(TOKENS[0])

    repo = gh.get_repo("osmlab/name-suggestion-index")
    issue = repo.get_issue(1881)
    assert (
        get_closer_commits(gh, issue)
        == repo.get_commits(author="bhousel", until=issue.closed_at).totalCount
    )
    issue = repo.get_issue(4957)
    assert (
        get_closer_commits(gh, issue)
        == repo.get_commits(author="kjonosm", until=issue.closed_at).totalCount
    )

    repo = gh.get_repo("HabitRPG/habitica")
    issue = repo.get_issue(12276)
    assert (
        get_closer_commits(gh, issue)
        == repo.get_commits(author="tsukimi2", until=issue.closed_at).totalCount
    )
    issue = repo.get_issue(12698)
    assert (
        get_closer_commits(gh, issue)
        == repo.get_commits(
            author="agarwalvaibhav0211", until=issue.closed_at
        ).totalCount
    )


def get_historical_issues(gh: Github, repo: Repository) -> List[dict]:
    """
    Estimate historical issue statistics using queries to GitHub, 
        which is accurate but may be costly.
    For performance reasons, we only collect issues that are created 3 months ago
    """
    since = datetime.now() - timedelta(days=90)
    issues = request_github(gh, lambda: repo.get_issues(state="closed", since=since))
    pages = page_num(gh.per_page, issues.totalCount)
    issue_stats = []
    logging.info(f"{repo.full_name}: {issues.totalCount} issues")
    for i in range(pages):
        curr_page: List[Issue] = request_github(gh, lambda: issues.get_page(i))
        logging.info(f"Collecting issue page {i}")
        for issue in curr_page:
            issue = request_github(gh, lambda: repo.get_issue(issue.number))
            if request_github(gh, lambda: "pull_request" in issue.raw_data):
                continue
            if issue.closed_at < since:
                continue
            issue_stat = {
                "number": issue.number,
                "created_at": issue.created_at.isoformat(),
                "closed_at": issue.closed_at.isoformat(),
                "closer_commit_num": get_closer_commits(gh, issue),
            }
            logging.debug(issue_stat)
            issue_stats.append(issue_stat)
    return issue_stats


def get_repo_metrics(gh: Github, repo: Repository) -> dict:
    """For a GitHub repostiory, get necessary data for GFI prediction"""
    open_prs = request_github(gh, lambda: repo.get_pulls(state="open").totalCount)
    closed_prs = request_github(gh, lambda: repo.get_pulls(state="closed").totalCount)
    open_issues = request_github(gh, lambda: repo.get_issues(state="open").totalCount)
    closed_issues = request_github(
        gh, lambda: repo.get_issues(state="closed").totalCount
    )
    return {
        "owner": repo.owner.login,
        "name": repo.name,
        "url": repo.url,
        "language": repo.language,
        "created": repo.created_at.isoformat(),
        "stars": repo.stargazers_count,
        "contributors": request_github(gh, lambda: repo.get_contributors().totalCount),
        "commits": request_github(gh, lambda: repo.get_commits().totalCount),
        "open_issues": open_issues - open_prs,
        "closed_issues": closed_issues - closed_prs,
        "open_prs": open_prs,
        "closed_prs": closed_prs,
        # "historical_issues": estimate_historical_issues(gh, repo),
        "historical_issues": get_historical_issues(gh, repo),
    }


def get_issue_metrics(gh: Github, repo: Repository, issue: Issue) -> dict:
    """For an issue in a GitHub repostiory, get necessary data for GFI prediction"""
    events = request_github(
        gh,
        lambda: [
            {"user": e.actor.login if e.actor is not None else None, "event": e.event}
            for e in list(issue.get_events())
        ],
        default=[],
    )
    comments = request_github(
        gh,
        lambda: [
            {"user": c.user.login, "body": c.body} for c in list(issue.get_comments())
        ],
        default=[],
    )
    return {
        "repo": repo.owner.login + "/" + repo.name,
        "number": issue.number,
        "url": issue.url,
        "user": issue.user.login,
        "title": issue.title,
        "body": issue.body,
        "labels": [l.name for l in issue.labels],
        "events": events,
        "comments": comments,
    }


def get_user_metrics(gh: Github, repo: Repository, user: NamedUser) -> dict:
    """For a user in a GitHub repostiory, get necessary data for GFI prediction"""
    repo_name = repo.owner.login + "/" + repo.name
    since = datetime.now() - timedelta(days=90)
    user_issues = request_github(
        gh,
        lambda: list(
            gh.search_issues(
                f"repo:{repo_name} is:issue author:{user.login} closed:>{since.isoformat()}"
            )
        ),
        default=[],
    )
    logging.info(
        f"Collecting profile for {user.login} who created {len(user_issues)} issues in {repo_name}"
    )
    return {
        "repo": repo_name,
        "user": user.login,
        "repos_owned": request_github(gh, lambda: user.get_repos().totalCount),
        "stars_received": request_github(
            gh,
            lambda: sum(
                r.stargazers_count
                for r in user.get_repos(sort="stars", direction="desc")
            ),
        ),
        "followers": request_github(gh, lambda: user.get_followers().totalCount),
        "commits_in_repo": request_github(
            gh,
            lambda: gh.search_commits(
                f"repo:{repo_name} author:{user.login}"
            ).totalCount,
        ),
        "commits_all": request_github(
            gh, lambda: gh.search_commits(f"author:{user.login}").totalCount
        ),
        "issues_in_repo": request_github(
            gh,
            lambda: gh.search_issues(
                f"repo:{repo_name} is:issue author:{user.login}"
            ).totalCount,
        ),
        "issues_all": request_github(
            gh, lambda: gh.search_issues(f"is:issue author:{user.login}").totalCount
        ),
        "pulls_in_repo": request_github(
            gh,
            lambda: gh.search_issues(
                f"repo:{repo_name} is:pr author:{user.login}"
            ).totalCount,
        ),
        "pulls_all": request_github(
            gh, lambda: gh.search_issues(f"is:pr author:{user.login}").totalCount
        ),
        "issue_closer_commits": [
            get_closer_commits(gh, i) for i in user_issues if i.state == "closed"
        ],
    }


def get_latest_issues(token: str, owner: str, name: str) -> Tuple[dict, list, list]:
    """
    The main worker function for a GitHub repository.
    Queries open issues in the past one month, and fetch necessary data for GFI prediction.
    """
    try:
        gh = Github(token)

        repo: Repository = request_github(gh, lambda: gh.get_repo(owner + "/" + name))
        latest_repo = get_repo_metrics(gh, repo)

        latest_issues = []
        issues: PaginatedList = request_github(
            gh,
            lambda: repo.get_issues(
                state="open",
                assignee="none",
                sort="created",
                direction="desc",
                since=datetime.now() - timedelta(days=7),
            ),
        )
        logging.info(f"{owner}/{name}: {issues.totalCount} latest issue/prs")

        for i in range(page_num(gh.per_page, issues.totalCount)):
            logging.info(f"Repo {owner}/{name}: collecting issue page {i}")
            issue_page: List[Issue] = request_github(gh, lambda: issues.get_page(i))
            for issue in issue_page:
                issue: Issue = request_github(gh, lambda: repo.get_issue(issue.number))
                if "pull_request" in issue.raw_data:
                    continue
                latest_issues.append(get_issue_metrics(gh, repo, issue))
        logging.info(f"{len(latest_issues)} available open issues collected")

        logging.info(f"Repo {owner}/{name}: collecting user data...")
        latest_users = []
        usernames = set([repo.owner.login])
        for issue in latest_issues:
            usernames.add(issue["user"])
            usernames.update([e["user"] for e in issue["events"]])
            usernames.update([c["user"] for c in issue["comments"]])
        logging.info(f"Repo {owner}/{name}: {len(usernames)} users, {usernames}...")
        for username in usernames:
            user = request_github(gh, lambda: gh.get_user(username))
            if user is not None:
                latest_users.append(get_user_metrics(gh, repo, user))

        logging.info(f"Finished collecting latest data for {owner}/{name}")
        with open(f"data/latest/{owner}_{name}.json", "w") as f:
            json.dump(
                {"repo": latest_repo, "issues": latest_issues, "users": latest_users},
                f,
                indent=2,
            )
        return latest_repo, latest_issues, latest_users
    except Exception as ex:
        logging.error(
            f"Error in get_latest_issues({token}, {owner}, {name}): "
            f"{ex}, {traceback.format_exc()}"
        )
        return None, [], []


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s (Process %(process)d) [%(levelname)s] %(filename)s:%(lineno)d %(message)s",
        level=logging.INFO,
    )

    pathlib.Path("data/latest/").mkdir(parents=True, exist_ok=True)

    projects = (
        pd.read_csv("data/proj_issues.csv")
        .sort_values(by="gfi_cnt", ascending=False)
        .head(100)
    )
    logging.info(f"Projects: \n{projects}")

    latest_issues = []
    latest_repos = []
    latest_users = []
    data = [
        (TOKENS[i % len(TOKENS)], owner, name)
        for i, (owner, name) in enumerate(zip(projects.owner, projects.name))
    ]
    with mp.Pool(len(TOKENS) * 3) as pool:
        results = pool.starmap(get_latest_issues, data)
    for repo, issues, users in results:
        if repo is not None:
            latest_repos.append(repo)
        latest_issues.extend(issues)
        latest_users.extend(users)

    with open("data/latest_issues.json", "w") as f:
        json.dump(latest_issues, f, indent=2)
    with open("data/latest_repos.json", "w") as f:
        json.dump(latest_repos, f, indent=2)
    with open("data/latest_users.json", "w") as f:
        json.dump(latest_users, f, indent=2)

    logging.info("Finish!")

