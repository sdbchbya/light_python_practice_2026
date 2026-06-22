import sys
import os


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
    print("Этап 1 выполнен успешно")


if __name__ == "__main__":
    main()