import os
from slowapi import Limiter
from slowapi.util import get_remote_address

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
    # Línea solo ejecutada en producción.
    # Instancia el limitador real de SlowAPI. No se testea directamente (# pragma: no cover)
    limiter = Limiter(  # pragma: no cover
        key_func=get_remote_address,
        default_limits=["3 per minute"]
    )
