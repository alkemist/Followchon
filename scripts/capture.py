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
write_capture_video = False
verbose = False
result_width = 1024
result_height = 768


model = YOLO('models/guinea-pig-v3+chons+camera-v2.pt')
live_path = 'live'
records_directory = 'records'
captures_directory = 'captures'
screens_directory = 'screens'
records_path = f"{live_path}/{records_directory}"
startTime = time.time()
global_traces = list()
stop = False

async def async_inference(_model, _frame, _save_results):
    results = _model(_frame, stream=True, verbose=False)
    image_result = detected_boxes_with_save(
        model,
        _frame,
        results,
        global_traces,
        f"{live_path}/{captures_directory}",
        f"{live_path}/{screens_directory}",
        _save_results,
        verbose,
        result_width,
        result_height,
    )

    cv2.imshow('Camera', image_result)



while not stop:
    records = list_files(records_path, r'.*\.(mkv)$')
    records_count = len(records)

    if records_count > 1:
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
                save_results = save_enabled and frameId % math.floor(frameRate) == 0

                asyncio.run(async_inference(model, frame, save_results))
                startTime = time.time()
            else:
                print(f"End record : {last_record}")

                if delete_record:
                    os.remove(camera_record_filename)

                break

            if cv2.waitKey(1) == ord('q'):
                stop = True

        cap.release()

cv2.destroyAllWindows()
