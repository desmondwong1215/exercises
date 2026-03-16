from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

MISSING_COMMENT = "No comment is found."

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # INSERT YOUR GRADING CODE HERE
    print("Starting verification...")
    if not exercise.repo.prs.pr.comments_from_user:
        raise exercise.wrong_answer([MISSING_COMMENT])
    return exercise.to_output(["Good job on adding a comment to the PR!"], GitAutograderStatus.SUCCESSFUL)

verify(GitAutograderExercise("C:\\Users\\User\\Documents\\git-mastery\\app\\gitmastery-exercises\\test-role-marker"))