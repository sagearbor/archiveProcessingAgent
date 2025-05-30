from __future__ import annotations

import os
from typing import Iterable, Set


class TokenAuthenticator:
    """Simple token-based authenticator."""

    def __init__(self, valid_tokens: Iterable[str] | None = None) -> None:
        token = os.getenv('AGENT_AUTH_TOKEN')
        self._tokens: Set[str] = set(valid_tokens or ([] if token is None else [token]))

    def is_authorized(self, token: str | None) -> bool:
        """Return ``True`` if the token is valid or auth is disabled."""
        if not self._tokens:
            return True
        if not token:
            return False
        return token in self._tokens
