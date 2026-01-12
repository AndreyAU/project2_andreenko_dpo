ALLOWED_TYPES = {"int", "str", "bool"}


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = [("ID", "int")]

    for column in columns:
        if ":" not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        name, col_type = column.split(":", 1)

        if col_type not in ALLOWED_TYPES:
            print(f"Некорректное значение: {col_type}. Попробуйте снова.")
            return metadata

        table_columns.append((name, col_type))

    metadata[table_name] = table_columns

    cols_str = ", ".join(f"{n}:{t}" for n, t in table_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')

    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def list_tables(metadata):
    if not metadata:
        print("Таблицы отсутствуют.")
        return

    for table in metadata:
        print(f"- {table}")

