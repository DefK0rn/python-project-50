import json
import re

import yaml

from gendiff.renders import render_json, render_plain, render_stylish


def load_file(file):

    match = re.search(r'(?<=\.)[a-zA-Z]{3,4}$', file)
    if not match:
        raise ValueError(f"Не удалось определить формат файла: {file}")
        
    file_extension = match.group(0).lower()

    with open(file, 'r', encoding='utf-8') as f:
        match file_extension:
            case 'json':
                return json.load(f)
            case 'yaml' | 'yml':
                return yaml.safe_load(f)
            case _:
                raise ValueError(f"Неподдерживаемый формат: {file_extension}")


def compare_dicts(old_dict, new_dict):

    all_keys = sorted(list(set(old_dict.keys()) | set(new_dict.keys())))
    diff = {}

    for key in all_keys:

        if key in old_dict and key not in new_dict:
            diff[key] = {'type': 'removed', 'value': old_dict[key]}
            
        elif key not in old_dict and key in new_dict:
            diff[key] = {'type': 'added', 'value': new_dict[key]}
            
        else:
            old_val = old_dict[key]
            new_val = new_dict[key]

            if isinstance(old_val, dict) and isinstance(new_val, dict):
                diff[key] = {
                    'type': 'nested',
                    'children': compare_dicts(old_val, new_val)
                }
            elif old_val == new_val:
                diff[key] = {'type': 'unchanged', 'value': new_val}
            else:
                diff[key] = {
                    'type': 'updated',
                    'old_value': old_val,
                    'new_value': new_val
                }

    return diff


def generate_diff(file1, file2, _format='stylish'):
    file_old = load_file(file1)
    file_new = load_file(file2)

    diff_tree = compare_dicts(file_old, file_new)

    match _format.lower():
        case 'plain':
            return render_plain(diff_tree)
        case 'json':
            return render_json(diff_tree)
        case _:
            return render_stylish(diff_tree)