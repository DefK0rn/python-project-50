import argparse

from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        usage='%(prog)s [-h] [-f FORMAT] first_file second_file',
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '-f', '--format',
        type=str,
        default='stylish',
        help='set format of output'
    )

    args = parser.parse_args()

    diff = generate_diff(args.first_file, args.second_file, args.format)
    print(diff)


if __name__ == "__main__":
    main()