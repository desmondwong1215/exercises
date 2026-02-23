"""Wrapper for Github CLI commands."""
# TODO: The following should be built using the builder pattern

from typing import Optional

from exercise_utils.cli import run


def fork_repo(
    repository_name: str,
    fork_name: str,
    verbose: bool,
    default_branch_only: bool = True,
) -> None:
    """
    Creates a fork of a repository.
    Forks only the default branch, unless specified otherwise.
    """
    command = ["gh", "repo", "fork", repository_name]
    if default_branch_only:
        command.append("--default-branch-only")
    command.extend(["--fork-name", fork_name])

    run(command, verbose)


def clone_repo_with_gh(
    repository_name: str, verbose: bool, name: Optional[str] = None
) -> None:
    """Creates a clone of a repository using Github CLI."""
    if name is not None:
        run(["gh", "repo", "clone", repository_name, name], verbose)
    else:
        run(["gh", "repo", "clone", repository_name], verbose)


def delete_repo(repository_name: str, verbose: bool) -> None:
    """Deletes a repository."""
    run(["gh", "repo", "delete", repository_name, "--yes"], verbose)


def create_repo(repository_name: str, verbose: bool) -> None:
    """Creates a Github repository on the current user's account."""
    run(["gh", "repo", "create", repository_name, "--public"], verbose)


def get_github_username(verbose: bool) -> str:
    """Returns the currently authenticated Github user's username."""
    result = run(["gh", "api", "user", "-q", ".login"], verbose)

    if result.is_success():
        username = result.stdout.splitlines()[0]
        return username
    return ""


def get_github_git_protocol(verbose: bool) -> str:
    """returns GitHub CLI's preferred Git transport protocol"""
    result = run(["gh", "config", "get", "git_protocol"], verbose)
    if result.is_success():
        protocol = result.stdout.splitlines()[0].strip()
        return protocol
    return ""


def has_repo(repo_name: str, is_fork: bool, verbose: bool) -> bool:
    """Returns if the given repository exists under the current user's repositories."""
    command = ["gh", "repo", "view", repo_name]
    if is_fork:
        command.extend(["--json", "isFork", "--jq", ".isFork"])
    result = run(
        command,
        verbose,
        env={"GH_PAGER": "cat"},
    )

    return result.is_success() and (not is_fork or result.stdout == "true")


def has_fork(
    repository_name: str, owner_name: str, username: str, verbose: bool
) -> bool:
    """Returns if the current user has a fork of the given repository by owner"""
    result = run(
        [
            "gh",
            "api",
            "--paginate",
            f"repos/{owner_name}/{repository_name}/forks",
            "-q",
            f'''.[] | .owner.login | select(. =="{username}")''',
        ],
        verbose,
    )

    return result.is_success() and result.stdout.strip() == username


def get_fork_name(
    repository_name: str, owner_name: str, username: str, verbose: bool
) -> str:
    """Returns the name of the current user's fork repo"""
    result = run(
        [
            "gh",
            "api",
            "--paginate",
            f"repos/{owner_name}/{repository_name}/forks",
            "-q",
            f'''.[] | select(.owner.login =="{username}") | .name''',
        ],
        verbose,
    )

    if result.is_success():
        forkname = result.stdout.splitlines()[0]
        return forkname
    return ""


def get_remote_url(repository_name: str, verbose: bool) -> str:
    """Returns a remote repo url based on the configured git protocol"""
    remote_url = f"https://github.com/{repository_name}.git"
    preferred_protocol = get_github_git_protocol(verbose)

    if preferred_protocol == "ssh":
        remote_url = f"git@github.com:{repository_name}.git"

    return remote_url


def create_pr(title: str, body: str, base: str, head: str, verbose: bool) -> str:
    """Create a pull request.

    Args:
        title: PR title
        body: PR description
        base: Base branch name
        head: Head branch name
        verbose: Enable verbose output

    Returns:
        PR URL if successful, empty string otherwise
    """
    command = [
        "gh",
        "pr",
        "create",
        "--title",
        title,
        "--body",
        body,
        "--base",
        base,
        "--head",
        head,
    ]

    result = run(command, verbose)

    if result.is_success():
        # Extract PR URL from output
        lines = result.stdout.strip().split("\n")
        for line in lines:
            if "https://github.com" in line:
                return line.strip()
    return ""


def view_pr(pr_number: int, verbose: bool) -> dict[str, str]:
    """View pull request details.

    Args:
        pr_number: PR number to view
        verbose: Enable verbose output

    Returns:
        Dictionary with PR details (title, body, state, etc.)
    """
    result = run(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--json",
            "title,body,state,author,headRefName,baseRefName",
        ],
        verbose,
    )

    if result.is_success():
        import json

        return json.loads(result.stdout)
    return {}


def comment_on_pr(pr_number: int, comment: str, verbose: bool) -> bool:
    """Add a comment to a pull request.

    Args:
        pr_number: PR number to comment on
        comment: Comment text
        verbose: Enable verbose output

    Returns:
        True if comment was added successfully, False otherwise
    """
    result = run(
        ["gh", "pr", "comment", str(pr_number), "--body", comment],
        verbose,
    )

    return result.is_success()


def list_prs(state: str, verbose: bool) -> list[dict[str, str]]:
    """List pull requests.

    Args:
        state: PR state filter ('open', 'closed', 'merged', 'all')
        verbose: Enable verbose output

    Returns:
        List of PR dictionaries with details
    """
    result = run(
        [
            "gh",
            "pr",
            "list",
            "--state",
            state,
            "--json",
            "number,title,state,author,headRefName,baseRefName",
        ],
        verbose,
    )

    if result.is_success():
        import json

        return json.loads(result.stdout)
    return []


def merge_pr(
    pr_number: int, merge_method: str, verbose: bool, delete_branch: bool = True
) -> bool:
    """Merge a pull request.

    Args:
        pr_number: PR number to merge
        merge_method: Merge method ('merge', 'squash', 'rebase')
        verbose: Enable verbose output
        delete_branch: Whether to delete the head branch after merge

    Returns:
        True if merge was successful, False otherwise
    """
    command = ["gh", "pr", "merge", str(pr_number), f"--{merge_method}"]

    if delete_branch:
        command.append("--delete-branch")

    result = run(command, verbose)
    return result.is_success()


def close_pr(pr_number: int, verbose: bool, comment: Optional[str] = None) -> bool:
    """Close a pull request without merging.

    Args:
        pr_number: PR number to close
        verbose: Enable verbose output
        comment: Optional comment to add when closing

    Returns:
        True if PR was closed successfully, False otherwise
    """
    command = ["gh", "pr", "close", str(pr_number)]

    if comment:
        command.extend(["--comment", comment])

    result = run(command, verbose)
    return result.is_success()


def review_pr(pr_number: int, comment: str, action: str, verbose: bool) -> bool:
    """Submit a review on a pull request.

    Args:
        pr_number: PR number to review
        comment: Review comment
        action: Review action ('approve', 'request-changes', 'comment')
        verbose: Enable verbose output

    Returns:
        True if review was submitted successfully, False otherwise
    """
    command = [
        "gh",
        "pr",
        "review",
        str(pr_number),
        "--body",
        comment,
        f"--{action}",
    ]

    result = run(command, verbose)
    return result.is_success()
