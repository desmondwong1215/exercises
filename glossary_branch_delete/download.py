from exercise_utils.git import clone_repo_with_git
from exercise_utils.github_cli import (
    delete_repo,
    fork_repo,
    get_github_username,
    has_repo,
)

TARGET_REPO = "git-mastery/samplerepo-funny-glossary"
FORK_NAME = "gitmastery-samplerepo-funny-glossary"


def setup(verbose: bool = False):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"
    
    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)
    
    fork_repo(TARGET_REPO, FORK_NAME, verbose, default_branch_only=False)
    
    clone_repo_with_git(f"https://github.com/{full_repo_name}", verbose, ".")
