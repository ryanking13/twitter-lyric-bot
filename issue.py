from github import Github
import config

g = Github(config.GITHUB_ACCESS_KEY)


def get_issue(repo_url, issue_no):
    issue = g.get_repo(repo_url).get_issue(number=issue_no)
    return issue.body


def update_issue(repo_url, issue_no, content):
    issue = g.get_repo(repo_url).get_issue(number=issue_no)
    issue.edit(body=issue.body + "\n" + content)

