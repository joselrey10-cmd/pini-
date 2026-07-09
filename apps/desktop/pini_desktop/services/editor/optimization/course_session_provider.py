from __future__ import annotations


class CourseSessionProvider:
    def __init__(self, repository):
        self.repository = repository

    def session_ids_for_course(self, course_id: int):
        sessions = self.repository.list_sessions()

        return [
            session.id
            for session in sessions
            if session.course_id == course_id
        ]