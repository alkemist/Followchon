# venv/bin/python -m src.dataset
import pathlib
import os
import shutil
import random

from .helpers.file import FileHelper

dataset_train_labels_path = './live/dataset/train/labels'
dataset_train_images_path = './live/dataset/train/images'
dataset_test_labels_path = './live/dataset/test/labels'
dataset_test_images_path = './live/dataset/test/images'
dataset_val_labels_path = './live/dataset/val/labels'
dataset_val_images_path = './live/dataset/val/images'

dataset_test_percent = 0.2
dataset_val_percent = 0.2

def extract(items, count):
    extracts = list()

    for i in range(count):
        choice = random.choice(items)
        extracts.append(pathlib.Path(choice).stem)

        items.remove(choice)

    return extracts


def moveTo(files, ext, src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for file in files:
        shutil.move(f"{src_dir}/{file}.{ext}",
                    f"{dst_dir}/{file}.{ext}")


annotations = FileHelper.list_files(dataset_train_labels_path, r'.*\.(txt)$').tolist()
train_count = len(annotations)
test_count = int(train_count * dataset_test_percent)
val_count = int(train_count * dataset_val_percent)

tests = extract(annotations, test_count)
moveTo(tests, 'txt', dataset_train_labels_path, dataset_test_labels_path)
moveTo(tests, 'jpg', dataset_train_images_path, dataset_test_images_path)

vals = extract(annotations, val_count)
moveTo(vals, 'txt', dataset_train_labels_path, dataset_val_labels_path)
moveTo(vals, 'jpg', dataset_train_images_path, dataset_val_images_path)


