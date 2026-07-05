from dataclasses import dataclass
from pathlib import Path

from openpyxl import Workbook, load_workbook

from pini_desktop.services.course_service import Course, CourseService
from pini_desktop.services.room_service import Room, RoomService
from pini_desktop.services.subject_service import Subject, SubjectService
from pini_desktop.services.teacher_service import Teacher, TeacherService


@dataclass(frozen=True)
class ImportResult:
    created_teachers: int = 0
    created_courses: int = 0
    created_subjects: int = 0
    created_rooms: int = 0
    errors: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.errors


class ExcelImportService:
    TEACHERS_SHEET = "Profesores"
    COURSES_SHEET = "Cursos"
    SUBJECTS_SHEET = "Materias"
    ROOMS_SHEET = "Aulas"

    def __init__(self, database_path=None):
        self.teacher_service = TeacherService(database_path) if database_path else TeacherService()
        self.course_service = CourseService(database_path) if database_path else CourseService()
        self.subject_service = SubjectService(database_path) if database_path else SubjectService()
        self.room_service = RoomService(database_path) if database_path else RoomService()

    def create_template(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        wb = Workbook()
        ws = wb.active
        ws.title = self.TEACHERS_SHEET
        ws.append(["codigo", "nombre", "apellidos", "especialidad", "horas_semanales", "max_sesiones_dia"])
        ws.append(["P01", "Ana", "García", "Primaria", 25, 5])

        ws = wb.create_sheet(self.COURSES_SHEET)
        ws.append(["codigo", "etapa", "nivel", "grupo", "alumnado"])
        ws.append(["1A", "Primaria", 1, "A", 22])

        ws = wb.create_sheet(self.SUBJECTS_SHEET)
        ws.append(["codigo", "nombre", "sesiones_semanales", "especialidad", "tipo_aula", "max_consecutivas", "doble_sesion"])
        ws.append(["LEN", "Lengua", 5, "Primaria", "Ordinaria", 1, "No"])

        ws = wb.create_sheet(self.ROOMS_SHEET)
        ws.append(["codigo", "nombre", "tipo", "capacidad", "edificio", "recursos", "disponible"])
        ws.append(["A1", "Aula 1", "Ordinaria", 25, "Principal", "", "Sí"])

        wb.save(path)
        return path

    def import_workbook(self, path: str | Path) -> ImportResult:
        wb = load_workbook(path)
        errors: list[str] = []
        created_teachers = created_courses = created_subjects = created_rooms = 0

        if self.TEACHERS_SHEET in wb.sheetnames:
            created, sheet_errors = self._import_teachers(wb[self.TEACHERS_SHEET])
            created_teachers += created
            errors.extend(sheet_errors)

        if self.COURSES_SHEET in wb.sheetnames:
            created, sheet_errors = self._import_courses(wb[self.COURSES_SHEET])
            created_courses += created
            errors.extend(sheet_errors)

        if self.SUBJECTS_SHEET in wb.sheetnames:
            created, sheet_errors = self._import_subjects(wb[self.SUBJECTS_SHEET])
            created_subjects += created
            errors.extend(sheet_errors)

        if self.ROOMS_SHEET in wb.sheetnames:
            created, sheet_errors = self._import_rooms(wb[self.ROOMS_SHEET])
            created_rooms += created
            errors.extend(sheet_errors)

        return ImportResult(
            created_teachers=created_teachers,
            created_courses=created_courses,
            created_subjects=created_subjects,
            created_rooms=created_rooms,
            errors=tuple(errors),
        )

    def _rows(self, worksheet):
        headers = [str(cell.value).strip().lower() if cell.value is not None else "" for cell in worksheet[1]]
        for row_index, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
            if all(value is None or str(value).strip() == "" for value in row):
                continue
            yield row_index, dict(zip(headers, row))

    def _import_teachers(self, worksheet):
        created = 0
        errors = []
        existing = {teacher.code for teacher in self.teacher_service.list_teachers()}
        for row_index, row in self._rows(worksheet):
            try:
                code = str(row.get("codigo") or "").strip()
                if not code or code in existing:
                    continue
                self.teacher_service.create_teacher(
                    Teacher(
                        id=None,
                        code=code,
                        name=str(row.get("nombre") or "").strip(),
                        surname=str(row.get("apellidos") or "").strip(),
                        speciality=str(row.get("especialidad") or "").strip(),
                        weekly_hours=int(row.get("horas_semanales") or 25),
                        max_daily_sessions=int(row.get("max_sesiones_dia") or 5),
                    )
                )
                existing.add(code)
                created += 1
            except Exception as exc:
                errors.append(f"Profesores fila {row_index}: {exc}")
        return created, errors

    def _import_courses(self, worksheet):
        created = 0
        errors = []
        existing = {course.code for course in self.course_service.list_courses()}
        for row_index, row in self._rows(worksheet):
            try:
                code = str(row.get("codigo") or "").strip()
                if not code or code in existing:
                    continue
                self.course_service.create_course(
                    Course(
                        id=None,
                        code=code,
                        stage=str(row.get("etapa") or "Primaria").strip(),
                        level=int(row.get("nivel") or 1),
                        group_name=str(row.get("grupo") or "A").strip(),
                        students=int(row.get("alumnado") or 25),
                    )
                )
                existing.add(code)
                created += 1
            except Exception as exc:
                errors.append(f"Cursos fila {row_index}: {exc}")
        return created, errors

    def _import_subjects(self, worksheet):
        created = 0
        errors = []
        existing = {subject.code for subject in self.subject_service.list_subjects()}
        for row_index, row in self._rows(worksheet):
            try:
                code = str(row.get("codigo") or "").strip().upper()
                if not code or code in existing:
                    continue
                self.subject_service.create_subject(
                    Subject(
                        id=None,
                        code=code,
                        name=str(row.get("nombre") or "").strip(),
                        weekly_sessions=int(row.get("sesiones_semanales") or 1),
                        required_speciality=str(row.get("especialidad") or "").strip(),
                        room_type=str(row.get("tipo_aula") or "").strip(),
                        max_consecutive=int(row.get("max_consecutivas") or 1),
                        allows_double_session=str(row.get("doble_sesion") or "").strip().casefold() in {"si", "sí", "yes", "true", "1"},
                    )
                )
                existing.add(code)
                created += 1
            except Exception as exc:
                errors.append(f"Materias fila {row_index}: {exc}")
        return created, errors

    def _import_rooms(self, worksheet):
        created = 0
        errors = []
        existing = {room.code for room in self.room_service.list_rooms()}
        for row_index, row in self._rows(worksheet):
            try:
                code = str(row.get("codigo") or "").strip().upper()
                if not code or code in existing:
                    continue
                self.room_service.create_room(
                    Room(
                        id=None,
                        code=code,
                        name=str(row.get("nombre") or "").strip(),
                        room_type=str(row.get("tipo") or "Ordinaria").strip(),
                        capacity=int(row.get("capacidad") or 25),
                        building=str(row.get("edificio") or "").strip(),
                        resources=str(row.get("recursos") or "").strip(),
                        available=str(row.get("disponible") or "Sí").strip().casefold() in {"si", "sí", "yes", "true", "1"},
                    )
                )
                existing.add(code)
                created += 1
            except Exception as exc:
                errors.append(f"Aulas fila {row_index}: {exc}")
        return created, errors
