from abc import ABC, abstractmethod

from .auth import AuthSession, EducaCyLCredentials
from .models import (
    CourseImport,
    ImportPackage,
    RoomImport,
    SchoolConfigurationImport,
    SubjectImport,
    TeacherImport,
)


class EducaCyLClient(ABC):
    @abstractmethod
    def authenticate(self, credentials: EducaCyLCredentials) -> AuthSession:
        raise NotImplementedError

    @abstractmethod
    def download_school_data(self) -> ImportPackage:
        raise NotImplementedError


class MockEducaCyLClient(EducaCyLClient):
    def __init__(self):
        self.session = AuthSession(authenticated=False)

    def authenticate(self, credentials: EducaCyLCredentials) -> AuthSession:
        self.session = AuthSession(authenticated=True, token=credentials.token or "mock-token")
        return self.session

    def download_school_data(self) -> ImportPackage:
        return ImportPackage(
            teachers=(
                TeacherImport("P01", "Ana", "García", "Primaria"),
                TeacherImport("P02", "Luis", "Pérez", "Inglés"),
            ),
            courses=(CourseImport("1A", "Primaria", 1, "A", 22),),
            subjects=(
                SubjectImport("LEN", "Lengua", 5, "Primaria", "Ordinaria"),
                SubjectImport("ING", "Inglés", 3, "Inglés", "Ordinaria"),
            ),
            rooms=(RoomImport("A1", "Aula 1", "Ordinaria", 25),),
            configuration=SchoolConfigurationImport(
                center_name="CEIP Tierra de Pinares",
                center_code="47001559",
                locality="Mojados",
                province="Valladolid",
            ),
            source="mock-educacyl",
        )
