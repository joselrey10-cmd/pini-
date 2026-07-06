from dataclasses import dataclass


@dataclass(frozen=True)
class EducaCyLCredentials:
    username: str
    password: str = ""
    token: str = ""


@dataclass(frozen=True)
class AuthSession:
    authenticated: bool
    token: str = ""
    provider: str = "mock"
