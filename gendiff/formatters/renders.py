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


def stringify(value, spaces_count=4):

    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return 'null'
    if not isinstance(value, dict):
        return str(value)

    current_indent = " " * spaces_count
    closing_indent = " " * (spaces_count - 4)
    
    lines = []
    for k, v in value.items():
        lines.append(f"{current_indent}{k}: {stringify(v, spaces_count + 4)}")
        
    return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"


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


def render_stylish(diff, spaces_count=2):

    prefix_indent = " " * spaces_count
    next_spaces_count = spaces_count + 4
    stringify_spaces = spaces_count + 2 + 4
    lines = []

    for key, node in diff.items():
        node_type = node['type']

        match node_type:
            case 'nested':
                lines.append(f"{prefix_indent}  {key}: {{")
                lines.append(
                    render_stylish(node['children'], next_spaces_count)
                )
                lines.append(f"{prefix_indent}  }}")
            case 'unchanged':
                val = stringify(node['value'], stringify_spaces)
                lines.append(f"{prefix_indent}  {key}: {val}")
            case 'added':
                val = stringify(node['value'], stringify_spaces)
                lines.append(f"{prefix_indent}+ {key}: {val}")
            case 'removed':
                val = stringify(node['value'], stringify_spaces)
                lines.append(f"{prefix_indent}- {key}: {val}")
            case 'updated':
                old_val = stringify(node['old_value'], stringify_spaces)
                new_val = stringify(node['new_value'], stringify_spaces)
                lines.append(f"{prefix_indent}- {key}: {old_val}")
                lines.append(f"{prefix_indent}+ {key}: {new_val}")

    if spaces_count == 2:
        return "{\n" + "\n".join(lines) + "\n}"
    return "\n".join(lines)