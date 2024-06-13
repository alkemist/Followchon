import pathlib
import shutil

from functions import list_files, read_lines

capture_directory = 'live/dataset/train/images'
annotations_directory = 'live/dataset/train/labels'
move_directory = 'live/errors'

captures = list_files(capture_directory, r'.*\.(jpg|jpeg|png)$')

norm_diff_error = 0.01

for f in captures:
    capture_name = pathlib.Path(f).stem
    capture_filename = pathlib.Path(f)
    annotation_path = f"{annotations_directory}/{capture_name}.txt"

    annotations = {}
    anonymes = list()
    chons = list()


    for line in read_lines(annotation_path):

        splitted_line = line.split(' ')
        index = int(splitted_line[0])
        points = splitted_line[1:]
        error = False

        if index == 0:
            for anonyme in anonymes:
                error = all(
                        abs(float(points[i]) - float(anonyme_coord)) < norm_diff_error
                        for i, anonyme_coord in enumerate(anonyme)
                    )
                if error:
                    break

            if error:
                print(f"- File '{capture_name}'")
                print(f"Duplicate guinea pig on {capture_name}")
            else:
                anonymes.append(points)
        else:
            for chon in chons:
                error = all(
                    abs(float(points[i]) - float(chon_coord)) < norm_diff_error
                    for i, chon_coord in enumerate(chon)
                )
                if error:
                    break

            if error:
                print(f"- File '{capture_name}'")
                print(f"Duplicate chon on {capture_name}")
            else:
                chons.append(points)

        if error:
            shutil.move(f"{capture_directory}/{capture_filename}",
                        f"{move_directory}/{capture_filename}")
            shutil.move(annotation_path,
                        f"{move_directory}/{capture_name}.txt")
            break


