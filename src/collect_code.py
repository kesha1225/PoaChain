import os


def collect_code(base_dir, output_file, extensions, ignore_dirs, ignore_files):
    """
    Собирает код из файлов с заданными расширениями в один файл, игнорируя указанные директории.

    :param base_dir: Директория для поиска файлов.
    :param output_file: Файл, в который будет записан результат.
    :param extensions: Список расширений файлов, которые нужно включить.
    :param ignore_dirs: Список директорий, которые нужно игнорировать.
    """
    with open(output_file, "w") as outfile:
        for dirpath, dirnames, filenames in os.walk(base_dir):
            # Удаление игнорируемых директорий из списка dirnames
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            for filename in filenames:
                if filename in ignore_files:
                    continue
                if any(filename.endswith(ext) for ext in extensions):
                    file_path = os.path.join(dirpath, filename)
                    outfile.write(f"\nФайл: {file_path}\n\n")
                    with open(file_path, "r") as file:
                        outfile.write(file.read() + "\n")


# Пример использования
base_directory = "."
output_filename = "all_code.txt"
extensions_to_include = [".py", ".js", ".html", ".css"]
ignore_directories = ["__pycache__", ".idea", ".venv"]
ignore_files = ["test.py", "test1.py", "test2.py", "test3.py", "test4.py"]

collect_code(
    base_directory,
    output_filename,
    extensions_to_include,
    ignore_directories,
    ignore_files,
)
