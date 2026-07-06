class EducaCyLError(Exception):
    pass


class AuthenticationError(EducaCyLError):
    pass


class DownloadError(EducaCyLError):
    pass


class ParseError(EducaCyLError):
    pass
