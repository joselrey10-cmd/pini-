from .models import ImportPackage


class EducaCyLParser:
    def parse(self, raw_data) -> ImportPackage:
        if isinstance(raw_data, ImportPackage):
            return raw_data
        raise TypeError("Formato no soportado todavía.")
