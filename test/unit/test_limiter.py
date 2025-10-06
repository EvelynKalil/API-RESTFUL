from app.core.limiter import DummyLimiter

class TestDummyLimiter:
    """Unit tests for DummyLimiter behavior in test environment."""

    TEST_RATE = "3/minute"
    EXPECTED_RETURN = "ok"
    SAMPLE_KEYWORD_VALUE = "sample"
    ASSERT_MESSAGE_ORIGINAL_RESULT = "The decorated function should return its original result."

    def test_limit_decorator_returns_function(self):
        """Should return the original function when decorated."""
        limiter = DummyLimiter()

        @limiter.limit(self.TEST_RATE)
        def sample_function():
            return self.EXPECTED_RETURN

        result = sample_function()
        assert result == self.EXPECTED_RETURN, self.ASSERT_MESSAGE_ORIGINAL_RESULT

    def test_any_method_returns_none(self):
        """Should return None for any undefined method accessed dynamically."""
        limiter = DummyLimiter()

        random_method_1 = limiter.any_random_name
        random_method_2 = limiter.another_random_method

        assert callable(random_method_1)
        assert callable(random_method_2)
        assert random_method_1() is None
        assert random_method_2(123, key=self.SAMPLE_KEYWORD_VALUE) is None
