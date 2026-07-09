from __future__ import annotations


class TeacherSessionProvider:
    def __init__(self, repository):
        self.repository = repository

    def session_ids_for_teacher(self, teacher_id: int):
        sessions = self.repository.list_sessions()

        return [
            session.id
            for session in sessions
            if session.teacher_id == teacher_id
        ]