from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, checkout, push, remove_remote
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    delete_repo,
    fork_repo,
    get_github_username,
    has_repo,
)
from exercise_utils.roles import RoleMarker


TARGET_REPO = "git-mastery/samplerepo-funny-glossary"
FORK_NAME = "gitmastery-samplerepo-funny-glossary"


def setup(verbose: bool = False):
    bob = RoleMarker("teammate-bob")
    alice = RoleMarker("teammate-alice")

    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"

    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    fork_repo(TARGET_REPO, FORK_NAME, verbose, False)
    clone_repo_with_gh(f"{username}/{FORK_NAME}", verbose, ".")
    remove_remote("upstream", verbose)
    checkout("PQR", True, verbose)

    # Bob adds a new glossary term
    create_or_update_file(
        "r.txt",
        "refactoring: Improving the code without changing what it does... in theory.\n",
    )
    add(["r.txt"], verbose)
    bob.commit("Add 'refactoring' to r.txt", verbose)

    # Bob pushes and creates a PR
    push("origin", "PQR", verbose)
    pr_url = bob.create_pr(
        "Add refactoring glossary term",
        "This PR adds the definition for refactoring to our funny glossary.",
        "main",
        "PQR",
        verbose,
    )

    if pr_url:

        # Alice reviews the PR
        alice.review_pr(1, "Looks good to me!", "comment", verbose)

        # Bob responds to the review
        bob.comment_on_pr(1, "Thanks for the review!", verbose)

