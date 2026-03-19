import json
from pathlib import Path
from unittest.mock import PropertyMock, patch

import pytest
from exercise_utils.test import assert_output
from git.repo import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderStatus,
    GitAutograderWrongAnswerException,
)
from git_autograder.helpers.pr_helper.pr_helper import PrHelper
from git_autograder.pr import GitAutograderPr

from .verify import MISSING_COMMENT, verify


@pytest.fixture
def exercise(tmp_path: Path) -> GitAutograderExercise:
    repo_dir = tmp_path / "ignore-me"
    repo_dir.mkdir()
    Repo.init(repo_dir)

    with open(tmp_path / ".gitmastery-exercise.json", "a") as config_file:
        config_file.write(
            json.dumps(
                {
                    "exercise_name": "test-role-marker",
                    "tags": [],
                    "requires_git": True,
                    "requires_github": True,
                    "base_files": {},
                    "exercise_repo": {
                        "repo_type": "local",
                        "repo_name": "ignore-me",
                        "init": True,
                        "create_fork": None,
                        "repo_title": None,
                        "pr_number": 1,
                        "pr_repo_full_name": "dummy/repo",
                    },
                    "downloaded_at": None,
                }
            )
        )

    with patch.object(
        PrHelper,
        "_fetch_pr_data",
        return_value={
            "title": "",
            "body": "",
            "state": "OPEN",
            "author": {"login": "dummy"},
            "baseRefName": "main",
            "headRefName": "feature",
            "isDraft": False,
            "mergedAt": None,
            "mergedBy": None,
            "latestReviews": [],
            "comments": [],
        },
    ):
        return GitAutograderExercise(exercise_path=tmp_path)


def test_verify_success_when_user_comments_exist(exercise: GitAutograderExercise):
    with patch.object(
        GitAutograderPr,
        "user_comments",
        new_callable=PropertyMock,
        return_value=["Looks good"],
    ):
        output = verify(exercise)

    assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_verify_fails_when_user_comments_missing(exercise: GitAutograderExercise):
    with (
        patch.object(
            GitAutograderPr,
            "user_comments",
            new_callable=PropertyMock,
            return_value=[],
        ),
        pytest.raises(GitAutograderWrongAnswerException) as exception,
    ):
        verify(exercise)

    assert exception.value.message == [MISSING_COMMENT]

    
