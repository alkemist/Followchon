import os
import re
import cv2
import math
from datetime import datetime
import random
import numpy
import shutil
from pathlib import Path


def detected_boxes_with_save(
        model, img_origine, results, global_traces,
        captures_dir,
        screens_dir,
        save_results=None, verbose=False,
        result_width=1024, result_height=768,
):
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{random.randint(0, 9)}"
    captures_labels_dir = f"{captures_dir}/labels"
    captures_images_dir = f"{captures_dir}/images"
    screens_path = f"{screens_dir}/{filename}"
    img_traced = img_origine.copy()
    logs, annotation_objs = list(), list()

    for r in results:
        boxes = r.boxes

        for box in boxes:
            (x1, y1, x2, y2, cls, label, conf) = get_box_info(model, box)
            (h_img, w_img) = img_origine.shape[:2]

            # Condition 1
            if conf > 0.60:
                yolo_points = calc_yolo_points(x1, y1, x2, y2, w_img, h_img)
                index = ['guinea pig', 'noisette', 'stitch'].index(label)

                coords_points = [
                    yolo_points['x_center'] - yolo_points['w'] / 2,
                    yolo_points['y_center'] - yolo_points['h'] / 2,
                    yolo_points['x_center'] + yolo_points['w'] / 2,
                    yolo_points['y_center'] + yolo_points['h'] / 2,
                ]

                annotation_objs.append(
                    {
                        'index': index,
                        'label': label,
                        'norm_points': coords_points,
                        'orth_points': [x1, y1, x2, y2],
                        'conf': conf,
                        'line':
                            f"{index} {yolo_points['x_center']} {yolo_points['y_center']} {yolo_points['w']} {yolo_points['h']}\n"
                    }
                )

    img_traced, validated_annotations = valid_annotations(img_traced, annotation_objs, logs)

    if len(validated_annotations) > 0 and verbose:
        logs.sort()
        if save_results:
            print(f"{filename} : ", logs)
        else:
            print(" " * 24, logs)

    if len(validated_annotations) > 0 and save_results:
        cv2.imwrite(f'{screens_path}.jpg', img_traced)

        if not os.path.exists(captures_images_dir):
            os.makedirs(captures_images_dir)

        img_reduced = resize_with_ratio(img_origine, result_width, result_height)
        cv2.imwrite(f'{captures_images_dir}/{filename}.jpg', img_reduced)

        validated_annotations.sort()

        file = Path(f'{captures_labels_dir}/{filename}.txt')
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("".join(validated_annotations))

    return resize_with_ratio(img_traced, result_width, result_height)


def valid_annotations(img, annotation_objs, logs):
    validated_annotations = list()

    norm_diff_duplicate_error = 0.1
    anonymes = list()
    chons = list()

    for annotation in annotation_objs:
        annotation['duplicate'] = False
        annotation['valid'] = False

        if annotation['index'] == 0:
            for anonyme in anonymes:
                # Condition 2 : Check is multiple guinea pig in the same place
                annotation['duplicate'] = all(
                    abs(float(annotation['norm_points'][i]) - float(anonyme_coord)) < norm_diff_duplicate_error
                    for i, anonyme_coord in enumerate(anonyme)
                )
                if annotation['duplicate']:
                    break
        else:
            for chon in chons:
                # Condition 2 : Check is multiple stitch/noisette in the same place
                annotation['duplicate'] = all(
                    abs(float(annotation['norm_points'][i]) - float(chon_coord)) < norm_diff_duplicate_error
                    for i, chon_coord in enumerate(chon)
                )
                if annotation['duplicate']:
                    break

        if not annotation['duplicate']:
            if annotation['index'] == 0:
                anonymes.append(annotation['norm_points'])
            else:
                chons.append(annotation['norm_points'])

        if not annotation['duplicate']:
            annotation['valid'] = True
            validated_annotations.append(annotation['line'])

        logs.append([annotation['index'], annotation['label'], annotation['conf'], annotation['valid']])

        img = trace_detected_box_coords(
            img,
            annotation['orth_points'][0], annotation['orth_points'][1],
            annotation['orth_points'][2],
            annotation['orth_points'][3],
            annotation['label'],
            annotation['conf'],
            2,
            (0, 0, 0),
            (255, 255, 255),
        )

    return img, validated_annotations


def detected_boxes_with_resize(
        model, img, results,
        result_width=1024, result_height=768,
):
    img_traced = detected_boxes(
        model, img, results,
        result_width
    )

    if result_width is not None and result_height is not None:
        img_traced = resize_with_ratio(img_traced, result_width, result_height)

    return img_traced


def detected_boxes(
        model, img, results,
        result_width=1024,
):
    img_traced = img.copy()
    (h, w) = img.shape[:2]
    font_scale = round(w / float(result_width)) \
        if result_width is not None \
        else 2

    for r in results:
        boxes = r.boxes
        for box in boxes:
            (img_traced, _) = trace_detected_box(
                model, img_traced, box, font_scale
            )

    return img_traced


def trace_detected_box(
        model, img, box, font_scale=2,
):
    (x1, y1, x2, y2, cls, label, conf) = get_box_info(model, box)

    return trace_detected_box_coords(
        img,
        x1, y1, x2, y2,
        label,
        conf,
        font_scale,
    )


def get_box_info(model, box):
    x1, y1, x2, y2 = box.xyxy[0]
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    conf = math.ceil((box.conf[0] * 100)) / 100
    cls = int(box.cls[0])
    label = model.names[cls]

    return x1, y1, x2, y2, cls, label, conf


def trace_detected_box_coords(
        img,
        x1,
        y1,
        x2,
        y2,
        label,
        score,
        font_scale=2,
        color_text=(0, 255, 0),
        color_bg=(255, 0, 255),
        font_thickness=2,
        font=cv2.FONT_HERSHEY_PLAIN,
):
    img_traced = img.copy()
    cv2.rectangle(
        img_traced,
        (x1, y1),
        (x2, y2),
        (255, 0, 255),
        2
    )

    score = str(round(float(score) * 100, 1)) + "%"
    text = "{}: {}".format(label, score)

    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size

    cv2.rectangle(img_traced, (x1, y1), (x1 + text_w + 10, y1 + text_h + 10), color_bg, -1)
    cv2.putText(img_traced, text, (x1 + 5, y1 + text_h + 5 + font_scale - 1), font, font_scale, color_text,
                font_thickness)

    return img_traced


def clean_list(array):
    return list(filter(None, array))


def read_lines(file_path):
    return numpy.sort(clean_list(
        open(file_path, "r").read().split("\n")
    ))


def resize_with_ratio(img_origine, width=None, height=None, inter=cv2.INTER_AREA):
    img_copy = img_origine.copy()
    (h, w) = img_copy.shape[:2]

    if width is None and height is None:
        return img_copy

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(img_copy, dim, interpolation=inter)


def list_files(path, regex):
    return numpy.sort([
        f
        for f
        in os.listdir(path)
        if re.search(regex, f)
    ])


def calc_yolo_points(x1, y1, x2, y2, w_img, h_img):
    (w_box, h_box) = x2 - x1, y2 - y1
    return {
        'x_center': (x1 + (w_box / 2)) / w_img,
        'y_center': (y1 + (h_box / 2)) / h_img,
        'w': w_box / w_img,
        'h': h_box / h_img,
    }


def calc_orthogonal_points(x_center_norm, y_center_norm, w_norm, h_norm, w_img, h_img):
    (w_box, h_box) = w_norm * w_img, h_norm * h_img
    return {
        'x1': round((x_center_norm * w_img) - (w_box / 2)),
        'y1': round((y_center_norm * h_img) - (h_box / 2)),
        'x2': round(x_center_norm * w_img + w_box / 2),
        'y2': round(y_center_norm * h_img + h_box / 2),
    }


def move_detection(_live_path, _captures_directory, _screens_directory, _dataset_directory, _capture_name):
    captures_path = f"{_live_path}/{_captures_directory}"
    dataset_path = f"{_live_path}/{_dataset_directory}"
    screens_path = f"{_live_path}/{_screens_directory}"

    shutil.move(f"{captures_path}/{_capture_name}.txt",
                f"{dataset_path}/train/labels/{_capture_name}.txt")
    shutil.move(f"{captures_path}/{_capture_name}.jpg",
                f"{dataset_path}/train/images/{_capture_name}.jpg")

    os.remove(f"{screens_path}/{_capture_name}.jpg")


def remove_detection(_live_path, _captures_directory, _screens_directory, _capture_name):
    captures_path = f"{_live_path}/{_captures_directory}"
    screens_path = f"{_live_path}/{_captures_directory}"

    os.remove(f"{captures_path}/{_capture_name}.txt")
    os.remove(f"{captures_path}/{_capture_name}.jpg")
    os.remove(f"{screens_path}/{_capture_name}.jpg")