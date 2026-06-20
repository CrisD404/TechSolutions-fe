import os

ALLOWED_ATTACHMENT_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "docx"}
MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10 MB por archivo


def _extension(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def _file_size(storage):
    storage.stream.seek(0, os.SEEK_END)
    size = storage.stream.tell()
    storage.stream.seek(0)
    return size


def validate_attachments(files):
    """Valida una lista de adjuntos (opcionales).

    Devuelve una tupla (ok, mensaje_error). Los inputs vacios se ignoran.
    """
    for storage in files:
        if not storage or not storage.filename:
            continue

        if _extension(storage.filename) not in ALLOWED_ATTACHMENT_EXTENSIONS:
            return False, (
                f"El archivo '{storage.filename}' tiene un formato no permitido. "
                "Formatos validos: PDF, JPG, PNG, DOCX."
            )

        if _file_size(storage) > MAX_ATTACHMENT_SIZE:
            return False, f"El archivo '{storage.filename}' supera el tamano maximo de 10MB."

    return True, None
