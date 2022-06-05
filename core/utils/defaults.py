import uuid


def generate_guid() -> str:
    return uuid.uuid4().hex
