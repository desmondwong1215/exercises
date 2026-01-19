from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

BRANCH_NOT_CREATED = "The local {branch} branch is not created."
BRANCH_NOT_TRACKING = "The local {branch} branch does not track origin/{branch}."
BRANCH_MISSING = "The local {branch} branch does not exist."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo = exercise.repo.repo  # git.Repo object
    errors = []

    # Step 1: Check local STU branch and tracking
    stu_branch = repo.heads.STU if hasattr(repo.heads, 'STU') else None
    if not stu_branch:
        errors.append(BRANCH_NOT_CREATED.format(branch="STU"))
    else:
        tracking = stu_branch.tracking_branch()
        if not tracking or tracking.name != 'origin/STU':
            errors.append(BRANCH_NOT_TRACKING.format(branch="STU"))

    # Step 2: Check local VWX branch and tracking
    vwx_branch = repo.heads.VWX if hasattr(repo.heads, 'VWX') else None
    if not vwx_branch:
        errors.append(BRANCH_NOT_CREATED.format(branch="VWX"))
    else:
        tracking = vwx_branch.tracking_branch()
        if not tracking or tracking.name != 'origin/VWX':
            errors.append(BRANCH_NOT_TRACKING.format(branch="VWX"))
            
    # Step 3: Check local ABC branch exists
    abc_branch = repo.heads.ABC if hasattr(repo.heads, 'ABC') else None
    if not abc_branch:
        errors.append(BRANCH_NOT_CREATED.format(branch="ABC"))
        
    # Step 4: Check local DEF branch exists
    def_branch = repo.heads.DEF if hasattr(repo.heads, 'DEF') else None
    if not def_branch:
        errors.append(BRANCH_NOT_CREATED.format(branch="DEF"))
        
    if errors:
        return exercise.to_output(errors, GitAutograderStatus.UNSUCCESSFUL)
    return exercise.to_output([
        "Great work! All required branches are present and correctly set up."
    ], GitAutograderStatus.SUCCESSFUL)
