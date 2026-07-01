import sys
import os

# Вывод справки
def print_help():
    help_text = """
ОБЩИЙ ФОРМАТ:
    python main.py <путь_к_папке> [-d <фильтр_папок>] [-f <фильтр_файлов>]

ОПИСАНИЕ ПАРАМЕТРОВ:
    <путь_к_папке>    - обязательный параметр, путь к папке, структуру которой нужно вывести
    -d <фильтр_папок> - опциональный параметр, фильтр для папок (выводятся только папки, 
                         содержащие указанную подстроку в названии)
    -f <фильтр_файлов> - опциональный параметр, фильтр для файлов (выводятся только файлы,
                         содержащие указанную подстроку в названии)

ПРИМЕРЫ ВЫЗОВА:
    python main.py /home/user/docs
    python main.py /home/user/docs -d project
    python main.py /home/user/docs -f .py
    python main.py /home/user/docs -d src -f .txt

ПРИМЕЧАНИЯ:
    - Фильтры регистронезависимые
    - Если корневая папка не соответствует фильтру папок, выводится предупреждение
    - В отчёте выводится статистика по отфильтрованным элементам
"""
    print(help_text)

# Рекурсивный обход папки с фильтрацией и сбором статистики
def print_directory_structure(path, indent=0, prefix="", folder_filter="", file_filter="", is_root=False):

    stats = {
        'files': 0,
        'folders': 0,
        'total_size': 0
    }

    # Если это корневая папка, проверяем её на соответствие фильтру
    if is_root:
        root_name = os.path.basename(path)
        if folder_filter != "" and folder_filter.lower() not in root_name.lower():
            # Корневая папка не проходит фильтр - выводим предупреждение и завершаем
            print(f"Внимание: корневая папка '{root_name}' не соответствует фильтру папок '{folder_filter}'")
            print("Обход завершён")
            return stats

    try:
        # Получаем список элементов в папке
        items = os.listdir(path)

        # Сортируем: сначала папки, потом файлы
        dirs = []
        files = []
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dirs.append(item)
            else:
                files.append(item)

        # Сортируем по алфавиту
        dirs.sort()
        files.sort()

        # Объединяем: сначала папки, потом файлы
        sorted_items = dirs + files

        # Проходим по всем элементам
        for i, item in enumerate(sorted_items):
            full_path = os.path.join(path, item)
            # is_last = (i == len(sorted_items) - 1)

            # Определяем символы для отображения структуры
            branch = "    "
            next_prefix = prefix + "    "

            # Обрабатываем папки
            if os.path.isdir(full_path):
                # Проверяем фильтр папок
                if folder_filter == "" or folder_filter.lower() in item.lower():
                    # Выводим папку
                    print(f"{prefix}{branch} {item}/")
                    stats['folders'] += 1

                    # Рекурсивно обходим вложенную папку
                    sub_stats = print_directory_structure(
                        full_path, indent + 1, next_prefix,
                        folder_filter, file_filter
                    )

                    # Суммируем статистику
                    stats['files'] += sub_stats['files']
                    stats['folders'] += sub_stats['folders']
                    stats['total_size'] += sub_stats['total_size']
                # else: папка не проходит фильтр - полностью пропускаем
            else:
                # Обрабатываем файлы
                # Проверяем фильтр файлов
                if file_filter == "" or file_filter.lower() in item.lower():
                    # Выводим файл
                    print(f"{prefix}{branch} {item}")
                    stats['files'] += 1

                    # Получаем размер файла
                    try:
                        size = os.path.getsize(full_path)
                        stats['total_size'] += size
                    except:
                        pass
                # else: файл не проходит фильтр - полностью пропускаем

    except PermissionError:
        print(f"{prefix}    !! Нет доступа к папке: {path}")
    except Exception as e:
        print(f"{prefix}    ! Ошибка при чтении: {path} - {e}")

    return stats

# Парсинг аргументов командной строки с проверкой корректности опций
def parse_arguments():
    args = sys.argv[1:]
    folder_path = None
    folder_filter = ""
    file_filter = ""

    i = 0
    while i < len(args):
        if args[i] == '-d' and i + 1 < len(args):
            folder_filter = args[i + 1]
            i += 2
        elif args[i] == '-f' and i + 1 < len(args):
            file_filter = args[i + 1]
            i += 2
        elif args[i].startswith('-'):
            # Обнаружена неизвестная опция
            print(f"Ошибка: неизвестная опция '{args[i]}'")
            print_help()
            sys.exit(1)
        else:
            # Если это не опция, считаем, что это путь к папке
            if folder_path is None:
                folder_path = args[i]
            i += 1

    return folder_path, folder_filter, file_filter


def main():
    # Если аргументов нет, выводим справку
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)

    # Парсим аргументы
    folder_path, folder_filter, file_filter = parse_arguments()

    # Проверяем, что передан путь к папке
    if folder_path is None:
        print("Ошибка: необходимо указать путь к папке")
        print_help()
        sys.exit(1)

    # Проверяем, существует ли указанная папка
    if not os.path.exists(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует")
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print(f"Ошибка: '{folder_path}' не является папкой")
        sys.exit(1)

    # Выводим информацию о запуске
    print(f"Программа успешно запущена")
    print(f"Путь к папке: {folder_path}")
    if folder_filter:
        print(f"Фильтр папок: '{folder_filter}'")
    if file_filter:
        print(f"Фильтр файлов: '{file_filter}'")

    # Выводим корневую папку
    root_name = os.path.basename(folder_path)
    print(f" {root_name}/")

    # Проверяем, соответствует ли корневая папка фильтру
    if folder_filter != "" and folder_filter.lower() not in root_name.lower():
        print(f"Внимание: корневая папка не соответствует фильтру папок '{folder_filter}'")
        print("Обход завершён")
        print("\n" + "=" * 50)
        print("ОТЧЁТ:")
        print("=" * 50)
        print(f"Количество обнаруженных папок: 0")
        print(f"Количество обнаруженных файлов: 0")
        print(f"Общий размер файлов: 0 байт")
        print("=" * 50)
        return

    # Выводим структуру папки и собираем статистику
    stats = print_directory_structure(
        folder_path,
        indent=0,
        prefix="",
        folder_filter=folder_filter,
        file_filter=file_filter,
        is_root=True  # Помечаем, что это корневая папка
    )

    print("Обход завершён")

    # Выводим отчёт
    print("")
    print("ОТЧЁТ:")
    print(f"Количество обнаруженных папок: {stats['folders']}")
    print(f"Количество обнаруженных файлов: {stats['files']}")
    print(f"Общий размер файлов: {stats['total_size']} байт")


if __name__ == "__main__":
    main()