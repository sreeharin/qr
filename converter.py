#!/usr/bin/env python

import sys
from qrcode import make

if __name__ == '__main__':
    try:
        assert len(sys.argv) > 1
    except AssertionError:
        print(f'usage: {sys.argv[0]} path_to_file')
        sys.exit(-1)

    file_path = sys.argv[1]
    file_contents = ""
    try:
        with open(file_path, 'r') as file:
            qr = make(file.read().strip())
            file_name = file_path.split('/')[-1]
            file_name = file_name.rsplit('.')[0]
            qr.save(f"{file_name}.png")
            print(f'Generated qr code from {file_path}')
    except FileNotFoundError:
        print("File not found!")
        sys.exit(-1)

