import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.constants import RATE_LIMIT_POST_MESSAGES

IS_TEST_ENV = os.getenv("TEST_ENV", "").lower() == "true"

if IS_TEST_ENV:
    class DummyLimiter:
        def limit(self, *_args, **_kwargs):
            """Return the original function unmodified (no rate limiting)."""
            def decorator(func):
                return func
            return decorator

        def __getattr__(self, _name):
            """Return a dummy callable that does nothing."""
            def dummy(*_args, **_kwargs):
                return None
            return dummy

    limiter = DummyLimiter()
else:
    # Executed only in production.
    # Instantiates the real SlowAPI limiter (excluded from test coverage)
    limiter = Limiter(  # pragma: no cover
        key_func=get_remote_address,
        default_limits=[RATE_LIMIT_POST_MESSAGES],
    )
