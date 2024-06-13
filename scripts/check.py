import pathlib
import cv2

# (g)uinea pig
# (n)oisette
# (s)titch
# (e)mpty
# (y)es
# (i)gnore
# (q)uit

from functions import list_files, read_lines, move_detection, remove_detection, calc_orthogonal_points, trace_detected_box_coords, \
    resize_with_ratio

check = False

live_path = 'live'
captures_directory = 'captures'
screens_directory = 'screens'
dataset_directory = 'dataset'
directory = f'{live_path}/{captures_directory}'
classes = ['guinea pig', 'noisette', 'stitch']
choices = [ord(c[0]) for c in classes]
stop = False

captures = list_files(directory, r'.*\.(txt)$')
captures_count = len(captures)

if not check:
    key = input('No check, juste move, (o)k ? ')
    if key != 'o':
        exit()

for capture_index, c in enumerate(captures):

    capture_name = pathlib.Path(c).stem
    annotation_path = f"{directory}/{capture_name}.txt"
    image_path = f"{directory}/{capture_name}.jpg"

    print(f"[{capture_index}/{captures_count}] File '{image_path}'")

    if not check:
        move_detection(live_path, captures_directory, screens_directory, dataset_directory, capture_name)
    else:
        base_img = cv2.imread(image_path)

        (h_img, w_img) = base_img.shape[:2]
        objects = list()

        for line in read_lines(annotation_path):
            splitted_line = line.split(' ')
            points = splitted_line[1:]
            float_points = [float(p) for p in points]

            if len(splitted_line) == 5:
                objects.append({
                    'index': int(splitted_line[0]),
                    'line': ' '.join(points),
                    'points': calc_orthogonal_points(
                        float_points[0], float_points[1], float_points[2], float_points[3],
                        w_img, h_img
                    )
                })
            else:
                print(f"Error on annotation file '{annotation_path}'")

        isAnonymous = all(o['index'] == 0 for o in objects)
        hasNoGuineaPigs = all(o['index'] != 0 for o in objects)
        newLines = list()

        for i, o in enumerate(objects):
            label = classes[o['index']]

            if not isAnonymous and o['index'] == 0:
                label = f"/!\ {label}"

            calculated_img = trace_detected_box_coords(
                base_img.copy(),
                o['points']['x1'],
                o['points']['y1'],
                o['points']['x2'],
                o['points']['y2'],
                label,
                0
            )
            calculated_img = resize_with_ratio(calculated_img, 1024, 768)

            winName = "Image"
            cv2.imshow(winName, calculated_img)

            cv2.namedWindow(winName)
            cv2.moveWindow(winName, 0, 0)

            while not stop:
                if not isAnonymous and o['index'] == 0:
                    print('Is (g)uineas pig or (e)mpty ?')

                    key = cv2.waitKey(0)

                    if key == ord('g') or key == ord('e') or key == ord('q'):
                        if key == ord('g'):
                            newLines.append(f"{o['index']} {o['line']}\n")
                        elif key == ord('q'):
                            stop = True
                        break
                elif not stop:
                    print('Is (n)oisette, (s)titch or (e)mpty ?')

                    key = cv2.waitKey(0)

                    if key == ord('s') or key == ord('n') or key == ord('e') or key == ord('q'):
                        if key == ord('e') or key == ord('q'):
                            if key == ord('q'):
                                stop = True
                            break

                        index = choices.index(key)

                        if isAnonymous:
                            newLines.append(f"{o['index']} {o['line']}\n")
                            newLines.append(f"{index} {o['line']}\n")
                            break
                        elif o['index'] > 0:
                            index = choices.index(key)
                            if hasNoGuineaPigs:
                                newLines.append(f"0 {o['line']}\n")
                            newLines.append(f"{index} {o['line']}\n")
                            break

            cv2.destroyAllWindows()

        if stop:
            break
        else:
            if len(newLines) > 0:
                newLines.sort()
                file = open(annotation_path, 'w')
                file.write("".join(newLines))

                move_detection(live_path, captures_directory, screens_directory, dataset_directory, capture_name)
            else:
                while True:
                    key = input('No detections, deletes files, (y)es or (i)gnore  ? ')

                    if key == 'y' or key == 'i':
                        if key == 'y':
                            remove_detection(live_path, captures_directory, screens_directory, capture_name)
                        break



