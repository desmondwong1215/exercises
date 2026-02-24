from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # INSERT YOUR GRADING CODE HERE
    print(exercise.read_config("pr_number"))
    print(exercise.read_config("teammate_role"))
    print(exercise.read_config("pr_url"))

    return exercise.to_output([], GitAutograderStatus.SUCCESSFUL)
