import os
import linecache
import re
from glob import glob
from collections import defaultdict

from typing import List, Tuple

from pipeline.sanitizers.regex import HAS_TAG, HAS_BOTH, HAS_CLOSING_TAG, HAS_OPENING_TAG

def annotate(raw_tokens) -> List[Tuple]:
    tokens = []
    current_label = 'other'
    for raw_token in raw_tokens:
        raw_token = raw_token.strip()

        if raw_token:
            has_tag = HAS_TAG.search(raw_token)
            if has_tag:
                has_both = HAS_BOTH.findall(raw_token)
                if has_both:
                    # print(f"raw_token: {raw_token} -> HB")
                    for (label, token) in has_both:
                        tokens.append((token, label))
                        # print(f"{token}~{label}")
                else:
                    has_opening = HAS_OPENING_TAG.search(raw_token)
                    has_closing = HAS_CLOSING_TAG.search(raw_token)

                    if has_opening:
                        token = has_opening.group('token')
                        label = has_opening.group('label')
                        # print(f"raw_token: {raw_token} -> HO")

                        # print(f"{has_opening.group('token')}~{has_opening.group('label')}")
                        current_label = has_opening.group('label')
                    elif has_closing:
                        token = has_closing.group('token')
                        label = has_closing.group('label')
                        # print(f"raw_token: {raw_token} -> HC")

                        # print(f"{has_closing.group('token')}~{has_closing.group('label')}")
                        current_label = 'other'
                    else:
                        print(f"Unable to find opening/closing tags for {raw_token}")
                        # print(f"raw_token: {raw_token} -> NEITHER")
                    if token:
                        tokens.append((token, label))
            else:
                # print(f"raw_token: {raw_token} -> NOTHING")
                tokens.append((raw_token, current_label))
        else:
            continue

    return tokens

# Materialise the style/idx to training data
def tokenise_idx(path_to_idx_files: str, path_to_sanitised_data: str):
    """
    path_to_idx_files (str): path to indices of each fold (globbable)
    path_to_data (str): path to files containing the annotated strings
    """
    idx_files = glob(os.path.abspath(path_to_idx_files))
    print(f"Reading indices from {path_to_idx_files}")
    print(f"Reading data from {path_to_sanitised_data}")

    folds = defaultdict(list)

    for file in idx_files:
        with open(file, 'r') as fh:
            style_idx = fh.read().strip('\n').split('\n')

            for idx in style_idx:
                fold_idx = file.split('/')[file.split('/').index('folds') + 1]

                csl_type, style, lineno = idx.split('/')

                filepath = os.path.join(path_to_sanitised_data, csl_type, style, 'output.sanitised.txt')

                line = linecache.getline(filepath, int(lineno))

                data = annotate(line.split(" "))

                folds[fold_idx].append(data)

    return folds

def main():
    current_directory = os.getcwd()

    annotated_path = os.path.join(current_directory, 'data/annotated')

    training_data = tokenise_idx(os.path.join(current_directory, 'data/training/folds/*/train_style_idx.txt'),
                                 annotated_path)

    val_data = tokenise_idx(os.path.join(current_directory, 'data/training/folds/*/val_style_idx.txt'),
                            annotated_path)

    def write_tokens_as_lines(data: list, file: str):
        with open(file, 'w') as fh:
            for t in data:
                for token, label in t:
                    fh.write(f"{token}\t{label}\n")
                fh.write('\n')

    for fold_idx, data in training_data.items():
        write_tokens_as_lines(data, os.path.join(current_directory, f"data/training/folds/{fold_idx}/train.txt"))

    for fold_idx, data in val_data.items():
        write_tokens_as_lines(data, os.path.join(current_directory, f"data/training/folds/{fold_idx}/val.txt"))

if __name__ == '__main__':
    main()
