from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

from exercise_utils.exercise_config import add_pr_config
from exercise_utils.github_cli import get_github_username, get_latest_pr_number_by_author


PR_MISSING = "No PR is found."
WRONG_BASE_BRANCH = "The PR's base branch is not 'main'."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = get_github_username(False)
    target_repo = f"git-mastery/{exercise.config.exercise_repo.repo_title}"
    pr_number = get_latest_pr_number_by_author(username, target_repo, False)
    if not pr_number:
        raise exercise.wrong_answer([PR_MISSING])
    
    add_pr_config(pr_number, target_repo, "/.gitmastery-exercise.json")
    exercise.fetch_pr()

    if exercise.repo.prs.pr.head_branch != "main":
        raise exercise.wrong_answer([WRONG_BASE_BRANCH])

    # event = GitAutograderPrEvent.PR_CREATED
    # if not exercise.repo.prs.pr.get_commits_after_event(event):
    #     raise exercise.wrong_answer([f"No commits are found after the PR was created. Please make sure to create the PR from the 'main' branch."])
    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)
