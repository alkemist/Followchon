# venv/bin/python -m src.check
import pathlib
import os
import cv2
from PIL import Image

from .helpers.file import FileHelper
from .helpers.image import ImageHelper

labels_path = './live/backup/labels'
images_path = './live/backup/images'
image_width = 1024
image_height = 768
active = True


annotations = FileHelper.list_files(labels_path, r'.*\.(txt)$').tolist()
images = FileHelper.list_files(images_path, r'.*\.(jpg|png)$').tolist()

for annotation in annotations:
    name = pathlib.Path(annotation).stem

    if not os.path.exists(f"{images_path}/{name}.jpg") and not os.path.exists(f"{images_path}/{name}.png"):
        print(f"Image don't exist", f"{images_path}/{name}")
        if active:
            os.remove(f"{labels_path}/{name}.txt")


for image in images:
    name = pathlib.Path(image).stem
    ext = pathlib.Path(image).suffix

    if not os.path.exists(f"{labels_path}/{name}.txt"):
        print(f"Annotation don't exist", f"{images_path}/{name}")

    image_file = cv2.imread(f"{images_path}/{image}")
    (h_img, w_img) = image_file.shape[:2]

    if h_img > image_height or w_img > image_width:
        print("Image too big", w_img, h_img, f"{images_path}/{image}")

        if active:
            cv2.imwrite(
                f"{images_path}/{image}",
                ImageHelper.resize_with_ratio(image_file, image_width, image_height)
            )

    if ext != '.jpg':
        print("Image not a jpg", f"{images_path}/{image}")

        if active:
            im = Image.open(f"{images_path}/{image}")
            rgb_im = im.convert('RGB')
            rgb_im.save(f"{images_path}/{name}.jpg")

            os.remove(f"{images_path}/{image}")
