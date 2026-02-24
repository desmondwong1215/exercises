from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

MISSING_COMMENT = "No comment is found."

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # INSERT YOUR GRADING CODE HERE
    print("Starting verification...")
    pr_number = exercise.read_config("pr_number")
    if pr_number is None:
        raise exercise.wrong_answer(["PR number is missing from config."])
    pr_number = int(pr_number)
    pr_data = exercise.view_pr(pr_number)
    print(pr_data)
    comments = pr_data["comments"]
    print(comments)
    print(comments[0]["body"])
    # user_comments = [comment for comment in comments if not RoleMarker.has_role_marker(comment["body"])]
    if not comments:
        raise exercise.wrong_answer([MISSING_COMMENT])
    return exercise.to_output(["Good job on adding a comment to the PR!"], GitAutograderStatus.SUCCESSFUL)

verify(GitAutograderExercise("C:\\Users\\User\\Documents\\git-mastery\\app\\gitmastery-exercises\\test-role-marker"))