import json
from typing import Any, Dict, List
from pathlib import Path

from exercise_utils.exercise_config import update_config_fields
from exercise_utils.file import create_or_update_file
from exercise_utils.git import add, checkout, push, remove_remote
from exercise_utils.github_cli import (
    clone_repo_with_gh,
    delete_repo,
    fork_repo,
    get_github_username,
    get_latest_pr_number_by_author,
    has_repo,
    list_prs,
    view_pr,
)
from exercise_utils.roles import RoleMarker


TARGET_REPO = "git-mastery/samplerepo-funny-glossary"
FORK_NAME = "gitmastery-samplerepo-funny-glossary"
METADATA_FILE = ".pr_metadata.json"


def setup(verbose: bool = False):
    print("hello")
    bob = RoleMarker("teammate-bob")
    alice = RoleMarker("teammate-alice")

    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"

    print(f"Setting up exercise repository for {username}...")
    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)

    print(f"Forking {TARGET_REPO} to {full_repo_name}...")
    fork_repo(TARGET_REPO, FORK_NAME, verbose, False)
    print("Fork created. Cloning the forked repository...")
    clone_repo_with_gh(f"{username}/{FORK_NAME}", verbose, ".")
    print("Repository cloned. Setting up branches and making changes...")
    remove_remote("upstream", verbose)
    print("Removed upstream remote to avoid confusion during exercise.")
    checkout("PQR", True, verbose)
    print("Checked out to new branch PQR. Now making changes and creating a PR...")

    # Bob adds a new glossary term
    print("Bob is adding a new glossary term...")
    create_or_update_file(
        "r.txt",
        "refactoring: Improving the code without changing what it does... in theory.\n",
    )
    add(["r.txt"], verbose)
    bob.commit("Add 'refactoring' to r.txt", verbose)

    # Bob pushes and creates a PR
    push("origin", "PQR", verbose)
    print("Bob pushed the branch to origin. Now creating a PR...")
    pr_number = bob.create_pr(
        "Add refactoring glossary term",
        "This PR adds the definition for refactoring to our funny glossary.",
        "main",
        "PQR",
        full_repo_name,
        verbose,
    )
    print(f"Created PR #{pr_number} at {full_repo_name}")

    if pr_number:
        # Alice reviews the PR
        alice.review_pr(pr_number, "Looks good to me!", "comment", full_repo_name, verbose)
        print(f"Alice reviewed PR #{pr_number}")
        # Bob responds to the review
        bob.comment_on_pr(pr_number, "Thanks for the review!", full_repo_name, verbose)
        print(f"Bob commented on PR #{pr_number}")
        alice.close_pr(pr_number, full_repo_name, comment="Closing the PR as it's just for testing purposes.", verbose=verbose)
        print(f"Alice closed PR #{pr_number}")

    try: 
        update_config_fields({
            "exercise_repo.pr_number": pr_number,
            "exercise_repo.repo_full_name": full_repo_name,
            "teammate_role": "teammate-bob",    
        })
    except Exception as e:
        print(f"Error updating config: {e}")
        raise e
    print("Setup complete. Configuration updated with PR details.")