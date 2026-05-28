from gendiff import generate_diff


FILE1_EMPTY = 'tests/file1_empty.json'
FILE2_EMPTY = 'tests/file2_empty.json'
FILE2_WITH_DATA = 'tests/file2_with_data.json'
FILE1_TEST= 'tests/file1_test.json'
FILE2_TEST = 'tests/file2_test.json'
FILE_EMPTY_RESULT = {
    'TXT': 'tests/file_empty_result.txt',
    'JSON': 'tests/file_empty_result_json.txt',
    'YAML': 'tests/file_empty_result_yaml.txt'
}
FILE_TEST_RESULT = {
    'TXT': 'tests/file_test_result.txt',
    'JSON': 'tests/file_test_result_json.txt',
    'YAML': 'tests/file_test_result_yaml.txt'
}
FILE_WITH_DATA_RESULT = {
    'TXT': 'tests/file_with_data_result.txt',
    'JSON': 'tests/file_with_data_result_json.txt',
    'YAML': 'tests/file_with_data_result_yaml.txt'
}
FORMATS = ['TXT', 'JSON', 'YAML']


def is_equal(file, text):

    with open(file, 'r') as f:
        content = f.read()

    return True if content == text else False


def test():

    first_files = [FILE1_EMPTY, FILE1_TEST, FILE1_EMPTY]
    second_files = [FILE2_EMPTY, FILE2_TEST, FILE2_WITH_DATA]
    result_files = [FILE_EMPTY_RESULT, FILE_TEST_RESULT, FILE_WITH_DATA_RESULT]

    for first_file, second_file, result_file in zip(first_files, second_files, result_files):
        for format in FORMATS:
            diff = str(generate_diff(first_file, second_file, format))
            assert is_equal(result_file[format], diff) == True