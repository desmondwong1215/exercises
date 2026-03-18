from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

from exercise_utils.exercise_config import add_pr_config
from exercise_utils.github_cli import get_github_username, get_latest_pr_number_by_author
from .download import TARGET_REPO

PR_MISSING = "No PR is found."

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = get_github_username(False)
    pr_number = get_latest_pr_number_by_author(username, TARGET_REPO, False)
    if not pr_number:
        raise exercise.wrong_answer([PR_MISSING])
    add_pr_config(pr_number, TARGET_REPO)
    exercise.fetch_pr()

    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)
