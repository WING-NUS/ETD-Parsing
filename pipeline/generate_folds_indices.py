import os
import subprocess
import random
from glob import glob

from sklearn.model_selection import KFold

# Directory structure
# <style>
# |_<data>-0.txt
# |_<data>-1.txt
# |_<data>-N.txt

# Path to the directory storing the sanitised outputs of each style by directories
PATH = os.path.join('/Users', 'yuanchuan', 'Downloads', 'data', 'ETD', 'annotated', 'journals')

def generate_folds(path: str, num_folds: int, frac: float, folds_location: str = 'folds'):
    """
    path (str): path to files with sanitised strings (globbable)
    num_folds (int): number of folds to create
    frac (float): fraction of the data to be use for generating the folds
    folds_location (str): location of the indices to be written to [default: 'folds/<fold_idx>']
    """
    files = glob(os.path.abspath(path))

    lengths = {}

    kf = KFold(n_splits=num_folds)

    for file in files:
        style = os.path.dirname(file).split('/')[-1]
        lengths[style] = int(subprocess.run(["wc", "-l", file], capture_output=True).stdout.strip().decode().split(' ')[0])

    for style, length in lengths.items():
        sampled_idx = random.sample(range(length), k=int(frac * length))

        for fold_idx, (train_idx, val_idx) in enumerate(kf.split(sampled_idx)):
            folds_directory = os.path.join(folds_location, str(fold_idx))
            if not os.path.exists(folds_directory):
                os.makedirs(folds_directory)

            with open(f"{folds_directory}/train_style_idx.txt", 'a') as train_file:
                for ti in train_idx:
                    train_file.write(f"{style}/{sampled_idx[ti]}\n")

            with open(f"{folds_directory}/val_style_idx.txt", 'a') as val_file:
                for vi in val_idx:
                    val_file.write(f"{style}/{sampled_idx[vi]}\n")

generate_folds(PATH + "/*/output.sanitised.txt", 10, 0.001)
