from pini_desktop.services.editor.optimization.teacher_session_provider import (
    TeacherSessionProvider,
)


class FakeSession:
    def __init__(self, session_id, teacher_id):
        self.id = session_id
        self.teacher_id = teacher_id


class FakeRepository:
    def list_sessions(self):
        return [
            FakeSession(1, 10),
            FakeSession(2, 20),
            FakeSession(3, 10),
        ]


def test_teacher_session_provider_returns_teacher_sessions():
    provider = TeacherSessionProvider(FakeRepository())

    assert provider.session_ids_for_teacher(10) == [1, 3]