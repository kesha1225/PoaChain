import os
import ast


def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    num_lines = len(lines)
    num_comments = sum(1 for line in lines if line.strip().startswith("#"))
    num_empty = sum(1 for line in lines if not line.strip())
    longest_line = max(lines, key=len, default="")
    total_length = sum(len(line) for line in lines)
    num_functions = sum(1 for line in lines if line.strip().startswith("def "))
    num_classes = sum(1 for line in lines if line.strip().startswith("class "))
    num_imports = sum(1 for line in lines if line.strip().startswith(("import ", "from ")))
    num_todos = sum(1 for line in lines if "TODO" in line or "FIXME" in line)
    num_decorators = sum(1 for line in lines if line.strip().startswith("@"))
    num_docstrings = sum(1 for line in lines if line.strip().startswith(('"""', "'''")))

    return {
        "num_lines": num_lines,
        "num_comments": num_comments,
        "num_empty": num_empty,
        "longest_line": len(longest_line),
        "total_length": total_length,
        "num_functions": num_functions,
        "num_classes": num_classes,
        "num_imports": num_imports,
        "num_todos": num_todos,
        "num_decorators": num_decorators,
        "num_docstrings": num_docstrings,
        "non_empty_non_comment_lines": num_lines - num_comments - num_empty
    }


def analyze_directory(directory):
    total_lines = 0
    total_comments = 0
    total_empty = 0
    longest_line_length = 0
    total_length = 0
    total_functions = 0
    total_classes = 0
    total_imports = 0
    total_todos = 0
    total_decorators = 0
    total_docstrings = 0

    for root, dirs, files in os.walk(directory):
        # Skip .venv and .idea directories
        dirs[:] = [d for d in dirs if d not in {'.venv', '.idea'}]

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                file_stats = analyze_file(filepath)

                total_lines += file_stats["num_lines"]
                total_comments += file_stats["num_comments"]
                total_empty += file_stats["num_empty"]
                longest_line_length = max(longest_line_length, file_stats["longest_line"])
                total_length += file_stats["total_length"]
                total_functions += file_stats["num_functions"]
                total_classes += file_stats["num_classes"]
                total_imports += file_stats["num_imports"]
                total_todos += file_stats["num_todos"]
                total_decorators += file_stats["num_decorators"]
                total_docstrings += file_stats["num_docstrings"]

    avg_line_length = total_length / total_lines if total_lines else 0

    return {
        "total_lines": total_lines,
        "total_comments": total_comments,
        "total_empty": total_empty,
        "longest_line_length": longest_line_length,
        "avg_line_length": avg_line_length,
        "non_empty_non_comment_lines": total_lines - total_comments - total_empty,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "total_imports": total_imports,
        "total_todos": total_todos,
        "total_decorators": total_decorators,
        "total_docstrings": total_docstrings
    }


if __name__ == "__main__":
    directory = "."
    stats = analyze_directory(directory)

    print(f"Общее количество строк: {stats['total_lines']}")
    print(f"Количество строк с комментариями: {stats['total_comments']}")
    print(f"Количество пустых строк: {stats['total_empty']}")
    print(f"Самая длинная строка: {stats['longest_line_length']}")
    print(f"Средняя длина строки: {stats['avg_line_length']:.2f}")
    print(f"Количество строк не учитывая пустые и комментарии: {stats['non_empty_non_comment_lines']}")
    print(f"Количество функций: {stats['total_functions']}")
    print(f"Количество классов: {stats['total_classes']}")
    print(f"Количество импортов: {stats['total_imports']}")
    print(f"Количество TODO/FIXME: {stats['total_todos']}")
    print(f"Количество декораторов: {stats['total_decorators']}")
    print(f"Количество докстрингов: {stats['total_docstrings']}")
