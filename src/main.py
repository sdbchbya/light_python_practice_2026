import sys
import os


def print_directory_structure(path, indent=0, prefix=""):
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
            is_last = (i == len(sorted_items) - 1)

            # Определяем символы для отображения структуры
            if is_last:
                branch = "    "
                next_prefix = prefix + "    "
            else:
                branch = "    "
                next_prefix = prefix + "    "

            # Выводим элемент с отступами
            if os.path.isdir(full_path):
                print(f"{prefix}{branch} {item}/")
                # Рекурсивно обходим вложенную папку
                print_directory_structure(full_path, indent + 1, next_prefix)
            else:
                # Получаем размер файла
                # try:
                #     size = os.path.getsize(full_path)
                #     size_str = f" ({size} bytes)"
                # except:
                #     size_str = ""
                print(f"{prefix}{branch} {item}")

    except PermissionError:
        print(f"{prefix}    !! Нет доступа к папке: {path}")
    except Exception as e:
        print(f"{prefix}    ! Ошибка при чтении: {path} - {e}")


def main():
    # Проверяем, что передан путь к папке
    if len(sys.argv) != 2:
        print("Ошибка: необходимо указать путь к папке")
        print("Пример: python main.py /путь/к/папке")
        sys.exit(1)

    folder_path = sys.argv[1]

    # Проверяем, существует ли указанная папка
    if not os.path.exists(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует")
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print(f"Ошибка: '{folder_path}' не является папкой")
        sys.exit(1)

    # Программа успешно запущена
    print(f"Программа успешно запущена")
    print(f"Путь к папке: {folder_path}")
    print(f" {os.path.basename(folder_path)}/")

    # Выводим структуру папки
    print_directory_structure(folder_path, indent=0, prefix="")

    print("Обход завершён")


if __name__ == "__main__":
    main()