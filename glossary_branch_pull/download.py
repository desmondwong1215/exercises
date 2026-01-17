import os
import time

from exercise_utils.cli import run_command
from exercise_utils.file import create_or_update_file
from exercise_utils.gitmastery import create_start_tag
from exercise_utils.git import add, add_remote, checkout, clone_repo_with_git, commit, push
from exercise_utils.github_cli import (
    get_github_username,
    fork_repo,
    has_repo,
    delete_repo,
)

TARGET_REPO = "git-mastery/samplerepo-funny-glossary"
FORK_NAME = "gitmastery-samplerepo-funny-glossary"
LOCAL_DIR = "funny-glossary"

__resources__ = {}


def setup(verbose: bool = False):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"

    # if has_repo(full_repo_name, True, verbose):
    #     delete_repo(full_repo_name, verbose)

    # fork_repo(TARGET_REPO, FORK_NAME, verbose, False)
    # print("Waiting for GitHub to process the fork...")
    # clone_repo_with_git(f"https://github.com/{full_repo_name}", verbose, LOCAL_DIR)

    # os.chdir(LOCAL_DIR)
    
    add_remote("origin", f"https://github.com/{full_repo_name}")
    run_command(["git", "fetch", "origin"], verbose)
    checkout("main", False, verbose)

    run_command(["git", "branch", "-dr", "origin/VWX"], verbose)

    checkout("ABC", False, verbose)
    run_command(["git", "reset", "--hard", "HEAD~1"], verbose)

    checkout("DEF", False, verbose)
    run_command(["git", "reset", "--hard", "HEAD~1"], verbose)
    create_or_update_file("e.txt", "documentation: Evidence that someone once cared.\n")
    add(["e.txt"], verbose)
    commit("Add 'documentation'", verbose)

