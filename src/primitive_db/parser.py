def parse_value(raw: str):
    raw = raw.strip()

    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False

    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]

    try:
        return int(raw)
    except ValueError:
        return raw


def parse_where(where_str: str) -> dict:
    """
    Пример:
    'age = 28' -> {'age': 28}
    'name = "Sergei"' -> {'name': 'Sergei'}
    """
    if "=" not in where_str:
        raise ValueError("Некорректное условие WHERE")

    field, value = where_str.split("=", 1)
    field = field.strip()
    value = parse_value(value)

    return {field: value}


def parse_set(set_str: str) -> dict:
    """
    Пример:
    'age = 29' -> {'age': 29}
    """
    return parse_where(set_str)

