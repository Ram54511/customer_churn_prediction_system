import hashlib
import hmac

# secret used to sign auth tokens; for a real deployment this would come
# from an environment variable, not source code
_SECRET = "churn-app-7f3k9x2m-change-me"


# create a signed token for a username
def make_token(username: str) -> str:
    sig = hmac.new(_SECRET.encode(), username.encode(), hashlib.sha256).hexdigest()[:32]
    return f"{username}:{sig}"


# verify a token and return the username, or None if invalid
def verify_token(token: str) -> str | None:
    if not token or ":" not in token:
        return None
    username, sig = token.rsplit(":", 1)
    expected = hmac.new(_SECRET.encode(), username.encode(), hashlib.sha256).hexdigest()[:32]
    if hmac.compare_digest(sig, expected):
        return username
    return None