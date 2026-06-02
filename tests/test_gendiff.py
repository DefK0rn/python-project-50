from gendiff import generate_diff


FILE1_EMPTY = 'tests/test_data/file1_empty.json'
FILE2_EMPTY = 'tests/test_data/file2_empty.json'
FILE2_WITH_DATA = 'tests/test_data/file2_with_data.json'
FILE1_TEST = 'tests/test_data/file1_test.json'
FILE2_TEST = 'tests/test_data/file2_test.json'
FILE1_EXT = 'tests/test_data/file1_ext.json'
FILE2_EXT = 'tests/test_data/file2_ext.json'
FILE_EMPTY_RESULT = {
    'STYLISH': 'tests/test_data/file_empty_result.txt',
    'PLAIN': 'tests/test_data/file_empty_result_plain.txt',
    'JSON': 'tests/test_data/file_empty_result_json.txt'
}
FILE_TEST_RESULT = {
    'STYLISH': 'tests/test_data/file_test_result.txt',
    'PLAIN': 'tests/test_data/file_test_result_plain.txt',
    'JSON': 'tests/test_data/file_test_result_json.txt'
}
FILE_WITH_DATA_RESULT = {
    'STYLISH': 'tests/test_data/file_with_data_result.txt',
    'PLAIN': 'tests/test_data/file_with_data_result_plain.txt',
    'JSON': 'tests/test_data/file_with_data_result_json.txt'
}
FILE_EXT_RESULT = {
    'STYLISH': 'tests/test_data/file_ext_result.txt',
    'PLAIN': 'tests/test_data/file_ext_result_plain.txt',
    'JSON': 'tests/test_data/file_ext_result_json.txt'
}
FORMATS = ['STYLISH', 'PLAIN', 'JSON']


def is_equal(file, text):

    with open(file, 'r') as f:
        content = f.read()

    return True if content == text else False


def test():

    first_files = [
        FILE1_EMPTY,
        FILE1_TEST,
        FILE1_EMPTY,
        FILE1_EXT
    ]
    second_files = [
        FILE2_EMPTY,
        FILE2_TEST,
        FILE2_WITH_DATA,
        FILE2_EXT
    ]
    result_files = [
        FILE_EMPTY_RESULT,
        FILE_TEST_RESULT,
        FILE_WITH_DATA_RESULT,
        FILE_EXT_RESULT
    ]

    for first_file, second_file, result_file in zip(first_files, second_files, result_files):
        for format in FORMATS:
            diff = str(generate_diff(first_file, second_file, format))
            assert is_equal(result_file[format], diff) == True