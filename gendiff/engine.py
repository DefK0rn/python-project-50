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
            diff[f"- {key}"] = format_value(old_dict[key])
            
        elif key not in old_dict and key in new_dict:
            diff[f"+ {key}"] = format_value(new_dict[key])
            
        else:
            old_val = old_dict[key]
            new_val = new_dict[key]

            if isinstance(old_val, dict) and isinstance(new_val, dict):
                inner_diff = compare_dicts(old_val, new_val)

                if inner_diff:
                    diff[f"  {key}"] = inner_diff
                else:
                    diff[f"  {key}"] = format_value(new_val)
                    
            elif old_val == new_val:
                diff[f"  {key}"] = format_value(new_val)
                
            else:
                diff[f"- {key}"] = format_value(old_val)
                diff[f"+ {key}"] = format_value(new_val)

    return diff


def format_value(val):

    if isinstance(val, bool):
        return str(val).lower()
    if isinstance(val, dict):
        return {k: format_value(v) for k, v in val.items()}
    
    return val


def generate_diff(file1, file2, _format='stylish'):
    file_old = load_file(file1)
    file_new = load_file(file2)

    diff_tree = compare_dicts(file_old, file_new)

    match _format.upper():
        case 'JSON':
            return json.dumps(diff_tree, indent=2, ensure_ascii=False)
        case 'YAML':
            return yaml.dump(diff_tree, sort_keys=False, allow_unicode=True)
        case _:
            return render_stylish(diff_tree)


def render_stylish(diff, depth=1):

    indent = "  " * depth
    bracket_indent = "  " * (depth - 1)
    lines = []

    for key, val in diff.items():

        if isinstance(val, dict):
            prefix = key[:2]
            clean_key = key[2:]
            lines.append(f"{bracket_indent}{prefix}{clean_key}: {{")
            lines.append(render_stylish(val, depth + 2))
            lines.append(f"{indent}}}")
        else:
            lines.append(f"{bracket_indent}{key}: {val}")

    if depth == 1:
        return "{\n" + "\n".join(lines) + "\n}"
    return "\n".join(lines)