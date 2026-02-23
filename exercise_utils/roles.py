import re
from contextlib import contextmanager
from typing import Callable, Generator, Optional

from exercise_utils import git


class RoleMarker:
    """Handles role marker formatting and extraction for collaborative workflows."""

    PATTERN = re.compile(r"^\[ROLE:([a-zA-Z0-9_-]+)\]\s*", re.IGNORECASE)

    def __init__(self) -> None:
        """Initialize RoleMarker."""
        self._active_role: Optional[str] = None
        self._original_functions: dict[str, Callable] = {}

    @staticmethod
    def format(role: str, text: str) -> str:
        """Format text with a role marker.
        Example: role='teammate-alice', text='Add feature' -> '[ROLE:teammate-alice] Add feature'
        """
        return f"[ROLE:{role}] {text}"

    @staticmethod
    def extract_role(text: str) -> Optional[str]:
        """Extract role name from text with role marker if present."""
        match = RoleMarker.PATTERN.match(text)
        return match.group(1).lower() if match else None

    @staticmethod
    def has_role_marker(text: str) -> bool:
        """Check if text contains a role marker."""
        return RoleMarker.PATTERN.match(text) is not None

    @staticmethod
    def strip_role_marker(text: str) -> str:
        """Remove role marker from text if present."""
        return RoleMarker.PATTERN.sub("", text)

    def _create_wrapper(
        self, original_func: Callable, text_param_index: int
    ) -> Callable:
        """Create a generic wrapper that adds role markers to a text parameter."""

        def wrapper(*args, **kwargs):
            args_list = list(args)

            if text_param_index < len(args_list):
                text = args_list[text_param_index]
                if self._active_role and not self.has_role_marker(text):
                    args_list[text_param_index] = self.format(self._active_role, text)

            return original_func(*args_list, **kwargs)

        return wrapper

    @contextmanager
    def as_role(self, role: str) -> Generator[None, None, None]:
        """Context manager to automatically apply role markers to git operations."""
        self._active_role = role
        self._original_functions = {
            "commit": git._commit_impl,
            "merge_with_message": git._merge_with_message_impl,
        }

        # Patch the implementation registry instead of the module namespace
        git._impl_registry["commit"] = self._create_wrapper(git._commit_impl, 0)
        git._impl_registry["merge_with_message"] = self._create_wrapper(
            git._merge_with_message_impl, 2
        )

        try:
            yield
        finally:
            # Clear the registry to restore original behavior
            git._impl_registry.pop("commit", None)
            git._impl_registry.pop("merge_with_message", None)
            
            self._original_functions.clear()
            self._active_role = None

    @property
    def active_role(self) -> Optional[str]:
        """Get the currently active role."""
        return self._active_role