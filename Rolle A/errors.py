class ImportErrorBase(Exception):
    pass


class FileNotFound(ImportErrorBase):
    pass


class InvalidDataFormat(ImportErrorBase):
    pass


class MissingFieldError(ImportErrorBase):
    pass