# venv/bin/python -m src.dataset
import pathlib
import os
import shutil
import random

from .helpers.file import FileHelper

dataset_backup_labels_path = './live/backup/labels'
dataset_backup_images_path = './live/backup/images'

dataset_test_labels_path = './live/dataset/test/labels'
dataset_test_images_path = './live/dataset/test/images'
dataset_val_labels_path = './live/dataset/val/labels'
dataset_val_images_path = './live/dataset/val/images'

dataset_train_labels_path = './live/dataset/train/labels'
dataset_train_images_path = './live/dataset/train/images'

dataset_test_percent = 0.2
dataset_val_percent = 0.2


def extract(items, count):
    extracts = list()

    for i in range(count):
        choice = random.choice(items)
        extracts.append(pathlib.Path(choice).stem)

        items.remove(choice)

    return extracts


def copyTo(files, ext, src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for file in files:
        if os.path.exists(f"{src_dir}/{file}.{ext}"):
            shutil.copy(f"{src_dir}/{file}.{ext}",
                        f"{dst_dir}/{file}.{ext}")


annotations = FileHelper.list_files(dataset_backup_labels_path, r'.*\.(txt)$').tolist()

backup_count = len(annotations)
test_count = int(backup_count * dataset_test_percent)
val_count = int(backup_count * dataset_val_percent)
train_count = backup_count - test_count - val_count

tests = extract(annotations, test_count)
copyTo(tests, 'txt', dataset_backup_labels_path, dataset_test_labels_path)
copyTo(tests, 'jpg', dataset_backup_images_path, dataset_test_images_path)

vals = extract(annotations, val_count)
copyTo(vals, 'txt', dataset_backup_labels_path, dataset_val_labels_path)
copyTo(vals, 'jpg', dataset_backup_images_path, dataset_val_images_path)

trains = extract(annotations, train_count)
copyTo(trains, 'txt', dataset_backup_labels_path, dataset_train_labels_path)
copyTo(trains, 'jpg', dataset_backup_images_path, dataset_train_images_path)


