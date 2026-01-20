from typing import List

from git import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

LOCAL_BRANCH_NOT_DELETED = "Local branch 'VWX' is not deleted"
REMOTE_BRANCH_NOT_DELETED = "Remote branch 'VWX' is not deleted"


def fetch_remotes(repo: Repo) -> None:
    """Fetch latest remote state with prune to remove stale references."""
    for remote in repo.remotes:
        remote.fetch(prune=True)


def get_remotes(repo: Repo) -> List[str]:
    """Get all remote branch references."""
    remote_branches = []
    for remote in repo.remotes:
        remote_branches.extend([ref.name for ref in remote.refs])
    return remote_branches


def has_remote(remotes: List[str], target: str) -> bool:
    """Check if a specific branch exists in remote branches."""
    return any(ref.endswith(f"/{target}") for ref in remotes)

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo: Repo = exercise.repo.repo
    comments = []

    if exercise.repo.branches.has_branch("VWX"):
        comments.append(LOCAL_BRANCH_NOT_DELETED)

    fetch_remotes(repo)
    remote_branches = get_remotes(repo)

    if has_remote(remote_branches, "VWX"):
        comments.append(REMOTE_BRANCH_NOT_DELETED)

    if comments:
        raise exercise.wrong_answer(comments)

    return exercise.to_output(
        ["Excellent! You successfully deleted the VWX branch from both local and remote!"],
        GitAutograderStatus.SUCCESSFUL,
    )
