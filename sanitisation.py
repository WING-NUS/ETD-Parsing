#!/usr/local/bin python

import mmap
import glob
import os
from multiprocessing import Pool

from tqdm import tqdm

from pipeline import sanitizers
from pipeline.sanitizers.definitions import DEFINITIONS

MAX_CPU = int(os.getenv('MAX_CPU', os.cpu_count() - 1))

def sanitise_file(file_path: str, output_filename: str = 'output.sanitised.txt'):
    """
    Sanitise the file based on the regular expressions defined.
    """
    if os.path.exists(file_path):
        csl_type, style = os.path.dirname(file_path).split('/')[-2:]

        with open(os.path.join(os.path.dirname(file_path), output_filename), 'w') as sout:
            with open(file_path, 'r+') as fin:
                with mmap.mmap(fin.fileno(), 0) as file_buffer:
                    total_lines = 0
                    while file_buffer.readline():
                        total_lines += 1

                    file_buffer.seek(0)

                    with tqdm(total=total_lines) as pbar:
                        line = file_buffer.readline()

                        pbar.set_description(f"Sanitising: {csl_type}/{style}")

                        while line:
                            decoded_line = line.decode()
                            sout.write(sanitizers.sanitise(decoded_line, DEFINITIONS[csl_type][style]))

                            line = file_buffer.readline()
                            pbar.update(1)
    else:
        raise FileNotFoundError(f"{file_path} not found.")

def main():
    # Change the path to where the BibTeX files are
    cwd = os.getcwd()
    files = glob.glob(os.path.join(cwd, 'data/annotated/*/*/output.no_invalid_rows.txt'))

    if not files:
        raise FileNotFoundError()

    with Pool(MAX_CPU) as pool:
        pool.map(sanitise_file, files)

if __name__ == '__main__':
    main()
