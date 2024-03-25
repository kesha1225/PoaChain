from web.constants import HTML_PATH


def get_html_file_data(filename: str) -> str:
    with open(f"{HTML_PATH}{filename}", "r") as f:
        return f.read()
