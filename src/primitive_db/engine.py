import shlex

from prettytable import PrettyTable

from .core import (
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from .parser import parse_set, parse_where
from .utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

META_FILE = "db_meta.json"


def run():
    print("\n***База данных***")
    print("Введите команду (help — справка)\n")

    while True:
        user_input = input("Введите команду: ").strip()
        if not user_input:
            continue

        args = shlex.split(user_input)
        command = args[0]
        params = args[1:]

        if command == "exit":
            print("До свидания!")
            break

        elif command == "help":
            print("\n***Процесс работы с таблицей***")
            print("<command> create_table <имя> <столбец:тип> ...")
            print("<command> insert into <table> values (...)")
            print("<command> select from <table> [where ...]")
            print("<command> delete from <table> where ...")
            print("<command> update <table> set ... where ...")
            print("<command> list_tables")
            print("<command> drop_table <имя>")
            print("<command> exit\n")

        elif command == "create_table":
            if len(params) < 2:
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = params[0]
            columns = params[1:]

            metadata = load_metadata(META_FILE) or {}
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILE, metadata)

        elif command == "insert":
            if len(params) < 4 or params[0] != "into" or params[2] != "values":
                print("Синтаксис: insert into <table> values (...)")
                continue

            table_name = params[1]
            values = params[3:]

            metadata = load_metadata(META_FILE)
            table_data = load_table_data(table_name)

            table_data = insert(metadata, table_name, values, table_data)
            save_table_data(table_name, table_data)

        elif command == "select":
            if len(params) < 2 or params[0] != "from":
                print("Синтаксис: select from <table> [where ...]")
                continue

            table_name = params[1]
            where_clause = None

            if len(params) > 2:
                if len(params) < 5 or params[2] != "where":
                    print(
                        "Синтаксис: select from <table> "
                        "where <field> = <value>"
                    )
                    continue

                where_str = " ".join(params[3:])

                try:
                    where_clause = parse_where(where_str)
                except ValueError as e:
                    print(e)
                    continue

            metadata = load_metadata(META_FILE)
            table_data = load_table_data(table_name)

            rows = select(table_data, where_clause)

            if not rows:
                print("Нет данных.")
                continue

            columns = [col for col, _ in metadata[table_name]]
            table = PrettyTable(columns)

            for row in rows:
                table.add_row([row[col] for col in columns])

            print(table)

        elif command == "delete":
            if len(params) < 4 or params[0] != "from" or params[2] != "where":
                print("Синтаксис: delete from <table> where <field> = <value>")
                continue

            table_name = params[1]
            where_str = " ".join(params[3:])

            try:
                where_clause = parse_where(where_str)
            except ValueError as e:
                print(e)
                continue

            table_data = load_table_data(table_name)
            new_data = delete(table_data, where_clause)

            if new_data is None:
                continue

            if len(new_data) == len(table_data):
                print("Удаление не выполнено.")
                continue

            save_table_data(table_name, new_data)
            print("Записи успешно удалены.")

        elif command == "update":
            if len(params) < 6 or params[1] != "set" or "where" not in params:
                print(
                    "Синтаксис: update <table> set <field> = <value> "
                    "where <field> = <value>"
                )
                continue

            table_name = params[0]
            where_index = params.index("where")

            set_str = " ".join(params[2:where_index])
            where_str = " ".join(params[where_index + 1 :])

            try:
                set_clause = parse_set(set_str)
                where_clause = parse_where(where_str)
            except ValueError as e:
                print(e)
                continue

            metadata = load_metadata(META_FILE)
            table_data = load_table_data(table_name)

            new_data = update(
                metadata,
                table_name,
                table_data,
                set_clause,
                where_clause,
            )

            if new_data is None:
                continue

            save_table_data(table_name, new_data)
            print("Записи успешно обновлены.")

        elif command == "list_tables":
            metadata = load_metadata(META_FILE)
            list_tables(metadata)

        elif command == "drop_table":
            if len(params) != 1:
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = params[0]
            metadata = load_metadata(META_FILE)
            metadata = drop_table(metadata, table_name)

            if metadata is None:
                continue

            save_metadata(META_FILE, metadata)

        else:
            print(f"Функции {command} нет. Попробуйте снова.")

