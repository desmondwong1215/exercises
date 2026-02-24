from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

from exercise_utils.github_cli import view_pr
from exercise_utils.roles import RoleMarker

MISSING_COMMENT = "No comment is found."

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # INSERT YOUR GRADING CODE HERE
    pr_data = view_pr(1, False)
    comments = pr_data["comments"]
    print(comments)
    print(comments[0]["body"])
    user_comments = [comment for comment in comments if not RoleMarker.has_role_marker(comment["body"])]
    if not user_comments:
        raise exercise.wrong_answer([MISSING_COMMENT])
    return exercise.to_output(["Good job on adding a comment to the PR!"], GitAutograderStatus.SUCCESSFUL)
