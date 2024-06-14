import cv2
from ultralytics import YOLO
import os
import asyncio
import math
import time
from datetime import datetime

from functions import list_files, detected_boxes_with_save, resize_with_ratio

#load_dotenv()
#live_stream_path = os.getenv('LIVE_STREAM_PATH')
# venv/bin/python scripts/capture.py

check_all_records = True
save_enabled = True
delete_record = True
delete_old_record = False
infinite = False
verbose = True

result_width = 1024
result_height = 768

write_capture_video = False

model = YOLO('models/guinea-pig-v3+chons+camera-v4.pt')
live_path = 'live'
records_directory = 'records'
captures_directory = 'captures'
screens_directory = 'screens'
records_path = f"{live_path}/{records_directory}"
stop = False

output = None
process = None
container = None

if write_capture_video:
    output_filename = f"{live_path}/output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    output = cv2.VideoWriter(
        f"{output_filename}.avi",
        cv2.VideoWriter_fourcc(*'X264'),
        30, (result_width, result_height))

    # fps = 0.1
    # process = sp.Popen(
    #     shlex.split(
    #     f'ffmpeg -y -s {result_width}x{result_height} -pixel_format bgr24 -f rawvideo -r {fps} -i pipe: -vcodec libx265 -pix_fmt yuv420p -crf 24 {output_filename}'),
    #                    stdin=sp.PIPE)
    #
    # container = av.open(output_filename, mode="w")
    # stream = container.add_stream("mpeg4", rate=1)
    # stream.width = result_width
    # stream.height = result_height
    # stream.pix_fmt = "yuv420p"

async def async_inference(frame, _save_results):
    results = model(frame, stream=True, verbose=False)

    image_result = detected_boxes_with_save(
        model,
        frame,
        results,
        f"{live_path}/{captures_directory}",
        f"{live_path}/{screens_directory}",
        _save_results,
        verbose,
        result_width,
        result_height,
    )

    if write_capture_video:
        print('ok')
        # output.write(image_result)

        # process.stdin.write(image_result.tobytes())

        # frame = av.VideoFrame.from_ndarray(image_result, format="rgb24")
        # for packet in stream.encode(frame):
        #     container.mux(packet)

    cv2.imshow('Camera', image_result)


while not stop:

    cap = cv2.VideoCapture("live/records/2024-06-14_10-00-00.mkv")
    records = list_files(records_path, r'.*\.(mkv)$')
    records_count = len(records)

    if records_count > 1 or not infinite and records_count > 0:
        last_record_index = records_count - 2 \
            if records_count > 2 and not check_all_records \
            else 0
        last_record = records[last_record_index]

        # Delete old records
        if delete_old_record:
            for i in range(last_record_index):
                print(f"Delete old record {records[i]}")
                os.remove(f"{records_path}/{records[i]}")

        camera_record_filename = f"{records_path}/{last_record}"

        print(f"Next record : {camera_record_filename}")

        cap = cv2.VideoCapture(camera_record_filename)

        frameRate = cap.get(5)  # frame rate

        while cap.isOpened() and not stop:
            nowTime = time.time()
            ret, frame = cap.read()

            if ret:
                frameId = cap.get(1)  # current frame number
                save_results = save_enabled # and frameId % math.floor(frameRate) == 0

                asyncio.run(async_inference(frame, save_results))
            else:
                print(f"End record : {last_record}")

                if delete_record:
                    os.remove(camera_record_filename)

                break

            if cv2.waitKey(1) == ord('q'):
                stop = True

        cap.release()

    elif not infinite:
        stop = True

if output is not None:
     output.release()

# if process is not None:
#     process.stdin.close()

# if container is not None:
#      container.close()

cv2.destroyAllWindows()
