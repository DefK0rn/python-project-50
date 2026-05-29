import json


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


def render_json(diff):

    return json.dumps(diff, indent=2, ensure_ascii=False)


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