from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

BRANCH_NOT_CREATED = "The local {branch} branch is not created."
BRANCH_NOT_TRACKING = "The local {branch} branch does not track origin/{branch}."
BRANCH_MISSING = "The local {branch} branch does not exist."
COMMIT_MISSING = "New commit in the remote {branch} branch is not pulled to the local {branch} branch."


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo = exercise.repo 
    comments = []

    # Step 1: Check local STU branch and tracking
    if not repo.branches.has_branch("STU"):
        comments.append(BRANCH_NOT_CREATED.format(branch="STU"))
    else:
        stu_branch = repo.branches.branch("STU").branch
        tracking = stu_branch.tracking_branch()
        if not tracking or tracking.name != 'origin/STU':
            comments.append(BRANCH_NOT_TRACKING.format(branch="STU"))

    # Step 2: Check local VWX branch and tracking
    if not repo.branches.has_branch("VWX"):
        comments.append(BRANCH_NOT_CREATED.format(branch="VWX"))
    else:
        vwx_branch = repo.branches.branch("VWX").branch
        tracking = vwx_branch.tracking_branch()
        if not tracking or tracking.name != 'origin/VWX':
            comments.append(BRANCH_NOT_TRACKING.format(branch="VWX"))
            
    # Step 3: Check local ABC branch exists and is up-to-date with origin/ABC
    if not repo.branches.has_branch("ABC"):
        comments.append(BRANCH_MISSING.format(branch="ABC"))
    else:
        # Check if origin/ABC exists
        abc_branch = repo.branches.branch("ABC").branch
        remote_abc = abc_branch.tracking_branch()
        if not remote_abc:
            comments.append(BRANCH_NOT_TRACKING.format(branch="ABC"))
        else:
            local_commits = set(commit.hexsha for commit in repo.branches.branch("ABC").commits)
            remote_commit_hexsha = remote_abc.commit.hexsha
            if remote_commit_hexsha not in local_commits:
                comments.append(COMMIT_MISSING.format(branch="ABC"))

    # Step 4: Check local DEF branch exists, is up-to-date, and has a merge commit
    if not repo.branches.has_branch("DEF"):
        comments.append(BRANCH_MISSING.format(branch="DEF"))
    else:
        def_branch = repo.branches.branch("DEF").branch
        remote_def = def_branch.tracking_branch()
        if not remote_def:
            comments.append(BRANCH_NOT_TRACKING.format(branch="DEF"))
        else:
            local_commits = set(commit.hexsha for commit in repo.branches.branch("DEF").commits)
            remote_commit_hexsha = remote_def.commit.hexsha
            if remote_commit_hexsha not in local_commits:
                comments.append(COMMIT_MISSING.format(branch="DEF"))
            # Check for merge commit (more than one parent)
            print(len(local_commits))
            # if len(local_commit.parents) < 2:
            #     comments.append("The local DEF branch does not have a merge commit (should result from pulling diverged branches).")

    if comments:
        return exercise.to_output(comments, GitAutograderStatus.UNSUCCESSFUL)
    return exercise.to_output([
        "Great work! All required branches are present and correctly set up."
    ], GitAutograderStatus.SUCCESSFUL)
