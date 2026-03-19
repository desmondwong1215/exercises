from pathlib import Path

from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

from exercise_utils.exercise_config import add_pr_config
from exercise_utils.github_cli import get_github_username, get_latest_pr_number_by_author


PR_MISSING = "No PR is found."
WRONG_HEAD_BRANCH = "The PR's head branch is not 'main'."
JAVA_FILE_MISSING = "Java.txt file is missing in the latest commit on main branch."
JAVA_INVALID_CONTENT = "The content in Java.txt in main branch is not correct."
EXPECTED_CONTENT_STEP_3 = ["1955, by James Gosling"]


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    username = get_github_username(False)
    target_repo = f"git-mastery/{exercise.config.exercise_repo.repo_title}"
    
    pr_number = get_latest_pr_number_by_author(username, target_repo, False)
    if not pr_number:
        raise exercise.wrong_answer([PR_MISSING])

    add_pr_config(pr_number, target_repo, Path("./"))
    exercise.fetch_pr()

    if exercise.repo.prs.pr.head_branch != "main":
        raise exercise.wrong_answer([WRONG_HEAD_BRANCH])

    latest_user_commit = exercise.repo.prs.pr.last_user_commit
    with latest_user_commit.file("Java.txt") as content:
        if content is None:
            raise exercise.wrong_answer([JAVA_FILE_MISSING])
        extracted_content = [line.strip() for line in content.splitlines() if line.strip() != ""]
    if extracted_content != EXPECTED_CONTENT_STEP_3:
        raise exercise.wrong_answer([JAVA_INVALID_CONTENT])

    return exercise.to_output(["Good job creating the PR and pushing commits!"], GitAutograderStatus.SUCCESSFUL)
