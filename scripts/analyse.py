import numpy
import pathlib
import json

from functions import list_files, read_lines


def analyse_dataset(base_dir, dataset_dir):
    images_annotations, labels = list(), list()
    dataset_path = f"{base_dir}/{dataset_dir}"

    images_filenames = list_files(dataset_path, r'.*\.(jpg|jpeg|png)$')

    labels_path = f"{dataset_path}/darknet.labels"

    if pathlib.Path(labels_path).is_file():
        labels = read_lines(labels_path)

    for f in images_filenames:
        annotations_array = list()
        annotation_path = f"{dataset_path}/{pathlib.Path(f).stem}.txt"

        # Get image size
        # im = Image.open(f"{dataset_path}/{f}")
        # width, height = im.size

        image_annotations = {
            "filename": f,
            # "width": width,
            # "height": height,
        }

        if pathlib.Path(annotation_path).is_file():
            for row in read_lines(annotation_path):
                row_splited = row.split(" ")
                index = int(row_splited[0])

                points = [
                    float(p)
                    for i, p
                    in enumerate(row_splited)
                    if i > 0
                ]

                points_splited = [points[i:i + 2] for i in range(0, len(points), 2)]
                # Points in pixel
                # points_splited = [[int(p[0] * width), int(p[1] * height)] for p in points if len(p) == 2]

                annotation = {
                    "label": labels[index],
                    "points": points_splited,
                }

                if (
                        index != float(row_splited[0])
                        or len(points) % 2 == 1
                        or len(points_splited) == 0
                        or len(points_splited) < 4
                        or len([
                    p
                    for p
                    in points
                    if p < 0 or p > 1
                ]) > 0
                ):
                    annotation['hasPointsError'] = True

                annotations_array.append(annotation)

            image_annotations['annotations'] = annotations_array

        if len(annotations_array) == 0:
            image_annotations['hasAnnotationsError'] = True

        images_annotations.append(image_annotations)

    return {
        "dirname": dataset_dir,
        "images": images_annotations,
    }


datasets_path = '../datasets'

dataset_dirs = numpy.sort([
    f.name
    for f
    in pathlib.Path(datasets_path).iterdir()
    if f.is_dir()
])

dataset_images = [
    analyse_dataset(datasets_path, d)
    for d in dataset_dirs
]

with open(f"{datasets_path}/report.json", 'w', encoding='utf-8') as f:
    json.dump(dataset_images, f, ensure_ascii=False, indent=1)
