class ConstraintEngine:
    def evaluate(self, solution):
        conflicts = []
        conflicts.extend(self._teacher_conflicts(solution))
        conflicts.extend(self._course_conflicts(solution))
        conflicts.extend(self._room_conflicts(solution))
        return conflicts

    def _teacher_conflicts(self, solution):
        seen = {}
        conflicts = []
        for session in solution.sessions:
            key = (session.teacher, session.day, session.period)
            if session.teacher and key in seen:
                conflicts.append(f"Profesor duplicado: {session.teacher} día {session.day} periodo {session.period}")
            seen[key] = session
        return conflicts

    def _course_conflicts(self, solution):
        seen = {}
        conflicts = []
        for session in solution.sessions:
            key = (session.course, session.day, session.period)
            if session.course and key in seen:
                conflicts.append(f"Curso duplicado: {session.course} día {session.day} periodo {session.period}")
            seen[key] = session
        return conflicts

    def _room_conflicts(self, solution):
        seen = {}
        conflicts = []
        for session in solution.sessions:
            key = (session.room, session.day, session.period)
            if session.room and key in seen:
                conflicts.append(f"Aula duplicada: {session.room} día {session.day} periodo {session.period}")
            seen[key] = session
        return conflicts
