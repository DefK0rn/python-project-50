import json
import re

import yaml


# for lowcase boolean values
def custom_bool_handler(pairs):

    return {k: (str(v).lower() if isinstance(v, bool) else v) for k, v in pairs}


def load_file(file):

    file_extention = re.search('(?<=\.)[a-zA-z]{4}$', file).group(0).lower()

    match file_extention:
        case 'json':
            return json.load(
                    open(file), object_pairs_hook=custom_bool_handler
                )
        case 'yaml':
            return yaml.safe_load(open(file))


def generate_diff(file1, file2, _format):

    file_old = load_file(file1)
    file_new = load_file(file2)

    merged = file_old | file_new
    merged = json.loads(json.dumps(merged, sort_keys=True))
    result = []

    for key, value in merged.items():
        new_value = str(file_new.get(key))
        old_value = str(file_old.get(key))
        
        if old_value == new_value:
            result.append((f"  {key}", new_value))
        else:
            if new_value != 'None':
                if old_value != 'None':
                    result.append((f"- {key}", old_value))
                result.append((f"+ {key}", new_value))
            else:
                if old_value != 'None':
                    result.append((f"- {key}", old_value))

    match _format:
        case 'JSON':
            return json.loads(json.dumps(dict(result), indent=2))
        case 'YAML':
            return yaml.dump(dict(result), sort_keys=False)
        case _:
            if result:
                result_beauty = list(
                        map(lambda item: f"  {item[0]}: {item[1]}", result)
                    )
                return '{\n' + '\n'.join(result_beauty) + '\n}'
            else:
                return '{}'