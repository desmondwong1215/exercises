# from exercise_utils.git import remove_remote
# from exercise_utils.github_cli import clone_repo_with_gh, delete_repo, fork_repo, get_github_username, has_repo
from exercise_utils.gitmastery import create_start_tag


TARGET_REPO = "git-mastery/gm-languages"
FORK_NAME = "gitmastery-languages"

def setup(verbose: bool = False):
    # username = get_github_username(verbose)
    # full_repo_name = f"{username}/{FORK_NAME}"

    # if has_repo(full_repo_name, True, verbose):
    #     delete_repo(full_repo_name, verbose)

    # fork_repo(TARGET_REPO, FORK_NAME, verbose, False)
    # clone_repo_with_gh(f"https://github.com/{username}/{FORK_NAME}", verbose, ".")
    # remove_remote("upstream", verbose)
    create_start_tag(verbose)
