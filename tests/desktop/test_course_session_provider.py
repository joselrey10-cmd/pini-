from pini_desktop.services.editor.optimization.course_session_provider import (
    CourseSessionProvider,
)


class FakeSession:
    def __init__(self, session_id, course_id):
        self.id = session_id
        self.course_id = course_id


class FakeRepository:
    def list_sessions(self):
        return [
            FakeSession(1, 10),
            FakeSession(2, 20),
            FakeSession(3, 10),
        ]


def test_course_session_provider_returns_course_sessions():
    provider = CourseSessionProvider(FakeRepository())

    assert provider.session_ids_for_course(10) == [1, 3]