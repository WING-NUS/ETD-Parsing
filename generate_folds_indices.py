import os
import subprocess
import random
from glob import glob
from collections import defaultdict

from sklearn.model_selection import KFold

# Directory structure
# <csl_type>/<style>/output.txt

# Minimum number of strings need to be sampled
TYPE_SAMPLE_RATE = {
    'thesis': 0.25,
    'journals': 0.005
}

def count_lines(file: str):
    """
    Use `wc` to count number of lines in the file
    """
    process = subprocess.run(["wc", "-l", file], capture_output=True)

    decoded_stdout = process.stdout.strip().decode()

    line_count = int(decoded_stdout.split(' ')[0])

    return line_count

def generate_folds(path: str, num_folds: int, folds_location: str = 'folds'):
    """
    path (str): path to files with sanitised strings (globbable)
    num_folds (int): number of folds to create
    frac (float): fraction of the data to be use for generating the folds
    folds_location (str): location of the indices to be written to [default: 'folds/<fold_idx>']
    """
    files = glob(os.path.abspath(path))

    line_counts_by_csl_type = defaultdict(dict)

    kf = KFold(n_splits=num_folds)

    for file in files:
        style = os.path.dirname(file).split('/')[-1]
        csl_type = os.path.dirname(file).split('/')[-2]
        line_counts_by_csl_type[csl_type][style] = count_lines(file)

    sampled_indices_by_csl_type = defaultdict(dict)

    for csl_type, styles_line_counts in line_counts_by_csl_type.items():
        for style, line_count in styles_line_counts.items():
            indices = random.sample(range(line_count),
                                    k=int(TYPE_SAMPLE_RATE[csl_type] * line_count))

            sampled_indices_by_csl_type[csl_type][style] = indices

    data = []

    for csl_type, styles_sampled_indices in sampled_indices_by_csl_type.items():
        for style, sampled_indices in styles_sampled_indices.items():
            for idx in sampled_indices:
                data.append(f"{csl_type}/{style}/{idx}")

    random.shuffle(data)

    folds = kf.split(data)

    for fold_idx, (train_indices, val_indices) in enumerate(folds):
        folds_directory = os.path.join(folds_location, str(fold_idx))
        if not os.path.exists(folds_directory):
            os.makedirs(folds_directory)

        with open(f"{folds_directory}/train_style_idx.txt", 'a') as train_file:
            for train_idx in train_indices:
                train_file.write(f"{data[train_idx]}\n")

        with open(f"{folds_directory}/val_style_idx.txt", 'a') as val_file:
            for val_idx in val_indices:
                val_file.write(f"{data[val_idx]}\n")

def main():
    current_directory = os.getcwd()

    # Path to the directory storing the sanitised outputs of each style by directories
    annotated_path = os.path.join(current_directory, 'data', 'annotated')

    generate_folds(os.path.join(annotated_path, "*/*/output.sanitised.txt"),
                   10, folds_location=os.path.join('data', 'training', 'folds'))

if __name__ == '__main__':
    main()
