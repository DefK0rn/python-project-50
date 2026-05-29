import json
import re

import yaml


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


def format_plain_value(val):

    if isinstance(val, bool):
        return str(val).lower()
    if val is None:
        return 'null'
    if isinstance(val, (dict, list)):
        return '[complex value]'
    if isinstance(val, str):
        return f"'{val}'"
    return str(val)


def format_stylish_value(val):

    if isinstance(val, bool):
        return str(val).lower()
    if val is None:
        return 'null'
    return val


def generate_diff(file1, file2, _format='stylish'):
    file_old = load_file(file1)
    file_new = load_file(file2)

    diff_tree = compare_dicts(file_old, file_new)

    match _format.lower():
        case 'plain':
            return render_plain(diff_tree)
        case 'json':
            return json.dumps(diff_tree, indent=2, ensure_ascii=False)
        case 'yaml':
            return yaml.dump(diff_tree, sort_keys=False, allow_unicode=True)
        case _:
            return render_stylish(diff_tree)


def render_stylish(diff, depth=1):

    indent = "  " * depth
    lines = []

    for key, node in diff.items():
        node_type = node['type']

        match node_type:
            case 'nested':
                lines.append(f"{indent}  {key}: {{")
                lines.append(render_stylish(node['children'], depth + 2))
                lines.append(f"{indent}  }}")
            case 'unchanged':
                val = format_stylish_value(node['value'])
                lines.append(f"{indent}  {key}: {val}")
            case 'added':
                val = format_stylish_value(node['value'])
                lines.append(f"{indent}+ {key}: {val}")
            case 'removed':
                val = format_stylish_value(node['value'])
                lines.append(f"{indent}- {key}: {val}")
            case 'updated':
                old_val = format_stylish_value(node['old_value'])
                new_val = format_stylish_value(node['new_value'])
                lines.append(f"{indent}- {key}: {old_val}")
                lines.append(f"{indent}+ {key}: {new_val}")

    if depth == 1:
        return "{\n" + "\n".join(lines) + "\n}"
    return "\n".join(lines)


def render_plain(diff, path=""):

    lines = []

    for key, node in diff.items():

        current_path = f"{path}.{key}" if path else key
        node_type = node['type']

        match node_type:
            case 'nested':
                lines.append(render_plain(node['children'], current_path))
            case 'added':
                val = format_plain_value(node['value'])
                lines.append(
                    f"Property '{current_path}' was added with value: {val}"
                )
            case 'removed':
                lines.append(f"Property '{current_path}' was removed")
            case 'updated':
                old_val = format_plain_value(node['old_value'])
                new_val = format_plain_value(node['new_value'])
                lines.append(
                    f"Property '{current_path}' was updated. " +
                    f"From {old_val} to {new_val}"
                )
            case 'unchanged':
                continue

    return "\n".join(filter(None, lines))