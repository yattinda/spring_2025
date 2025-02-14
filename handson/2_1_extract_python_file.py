# python3 2_1_extract_python_file.py ../datasets/raw/Numpy -o  numpy.txt
import os
import argparse

def list_python_files(directory):
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def write_python_files_to_txt(directory, output_file='python_files.txt'):
    python_files = list_python_files(directory)
    with open(os.path.join('../datasets/correct_python_file/', output_file), 'w') as file:
        for item in python_files:
            file.write("%s\n" % item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List and save .py files from a directory.')
    parser.add_argument('directory', type=str, help='The path to the directory containing .py files.')
    parser.add_argument('-o', '--output', type=str, default='python_files.txt', help='The output file name (default: python_files.txt)')

    args = parser.parse_args()
    write_python_files_to_txt(args.directory, args.output)
