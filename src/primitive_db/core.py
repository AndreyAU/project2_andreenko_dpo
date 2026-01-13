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

def insert(metadata, table_name, values, table_data):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data or []

    if table_data is None:
        table_data = []

    schema = metadata[table_name]
    columns = schema[1:]  # без ID

    if len(values) != len(columns):
        print("Некорректное количество значений.")
        return table_data

    cleaned_values = []
    for v in values:
        v = v.strip().strip(",")
        if v.startswith("("):
            v = v[1:]
        if v.endswith(")"):
            v = v[:-1]
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        cleaned_values.append(v)

    new_id = max((row["ID"] for row in table_data), default=0) + 1

    record = {"ID": new_id}

    for (col_name, col_type), value in zip(columns, cleaned_values):
        try:
            if col_type == "int":
                value = int(value)
            elif col_type == "bool":
                value = value.lower() in ("true", "1")
            elif col_type == "str":
                value = str(value)
        except ValueError:
            print(f"Некорректное значение: {value} для типа {col_type}")
            return table_data

        record[col_name] = value

    table_data.append(record)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')

    return table_data




def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    result = []

    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in row or row[key] != value:
                match = False
                break

        if match:
            result.append(row)

    return result


def update(table_data, set_clause, where_clause):
    updated = False

    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in row or row[key] != value:
                match = False
                break

        if match:
            for key, value in set_clause.items():
                row[key] = value
            updated = True

    if not updated:
        print("Подходящие записи не найдены.")

    return table_data


   

def delete(table_data, where_clause):
    new_data = []
    deleted = False

    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if key not in row or row[key] != value:
                match = False
                break

        if match:
            deleted = True
        else:
            new_data.append(row)

    if not deleted:
        print("Подходящие записи не найдены.")

    return new_data




def list_tables(metadata):
    if not metadata:
        print("Таблицы отсутствуют.")
        return

    for table in metadata:
        print(f"- {table}")

