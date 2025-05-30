from src.agent.authentication import TokenAuthenticator


def test_is_authorized():
    auth = TokenAuthenticator(valid_tokens=["token123"])
    assert auth.is_authorized("token123")
    assert not auth.is_authorized("wrong")
    assert not auth.is_authorized(None)

