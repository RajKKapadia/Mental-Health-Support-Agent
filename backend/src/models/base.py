import uuid


from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def generate_uuid():
    """
    Generate a unique UUID for database records
    """
    return str(uuid.uuid4())
