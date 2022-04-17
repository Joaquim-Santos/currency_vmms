import os
import json

from currency_vmms_api.common.exceptions import EntityNotFound


def get_log_files(folder):
    return [file_name for file_name in os.listdir(folder)]


def load_file(folder, filename, is_json=False):
    full_path = os.path.join(folder, filename)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as file:
            if is_json:
                content = json.load(file)
            else:
                content = file.read()
    else:
        raise EntityNotFound(f"Arquivo {filename} não encontrado.")

    return content
