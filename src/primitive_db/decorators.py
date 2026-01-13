import time
from functools import wraps


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except FileNotFoundError:
            print(
                "Ошибка: файл данных не найден. "
                "Возможно, таблица не существует или база не инициализирована."
            )

        except KeyError as e:
            print(f"Ошибка: таблица или поле '{e}' не найдено.")

        except ValueError as e:
            print(f"Ошибка валидации: {e}")

        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

        return None

    return wrapper


def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            ).strip().lower()

            if answer != "y":
                print("Операция отменена.")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator




def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция {func.__name__} выполнилась за {end - start:.3f} секунд.")
        return result
    return wrapper
