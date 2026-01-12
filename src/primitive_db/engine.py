import shlex

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata

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
            print("<command> list_tables")
            print("<command> drop_table <имя>")
            print("<command> exit\n")

        elif command == "create_table":
            if len(params) < 2:
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = params[0]
            columns = params[1:]

            metadata = load_metadata(META_FILE)
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILE, metadata)

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
            save_metadata(META_FILE, metadata)

        else:
            print(f"Функции {command} нет. Попробуйте снова.")

