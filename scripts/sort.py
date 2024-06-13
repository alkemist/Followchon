import pathlib
import shutil

from functions import list_files, read_lines

annotations_directory = 'live/captures'
annotations = list_files(annotations_directory, r'.*\.txt$')

for f in annotations:
    annotation_path = f"{annotations_directory}/{pathlib.Path(f)}"
    lines = read_lines(annotation_path)
    lines.sort()

    file = open(annotation_path, 'w')
    file.write("\n".join(lines))
