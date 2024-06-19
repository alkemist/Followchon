import os
import cv2
import math
import subprocess

from ..helpers.file import FileHelper
from .model import Model


class Streamer:

    def __init__(
            self,
            stream_path,
            model_path,
            records_directory,
            captures_directory,
            capture_width=1024,
            capture_height=768,
            check_all_records=False,
            delete_record=False,
            loop_enabled=False,
            save_enabled=False,
            verbose=False,
            show_stream=False,
    ):
        self.check_all_records = check_all_records
        self.delete_record = delete_record
        self.loop_enabled = loop_enabled
        self.save_enabled = save_enabled
        self.verbose = verbose
        self.show_stram = show_stream

        self.stop = False
        self.stream_path = stream_path
        self.records_directory = records_directory
        self.captures_directory = captures_directory

        self.model = Model(model_path, capture_width, capture_height)

    def record(self):
        command = (f"ffmpeg -hide_banner -y -loglevel error -rtsp_transport tcp -use_wallclock_as_timestamps "
                   f"1 -i {self.stream_path} -vcodec copy -acodec copy -f segment -reset_timestamps 1 "
                   f"-segment_time 60 -segment_format mkv -segment_atclocktime 1 -strftime 1 "
                   f"{self.records_directory}/%Y-%m-%d_%H-%M-%S.mkv")

        return subprocess.Popen(command.split(" "),
                                stdout=subprocess.PIPE,
                                universal_newlines=True)

    def start(self):
        process = self.record()

        last_record_index = 0
        records = FileHelper.list_files(self.records_directory, r'.*\.(mkv)$')
        records_count = len(records)

        while not self.stop:
            return_code = process.poll()

            if return_code is not None:
                if self.verbose:
                    print('Restart recording')
                process = self.record()

            if self.delete_record:
                records = FileHelper.list_files(self.records_directory, r'.*\.(mkv)$')
                records_count = len(records)

                last_record_index = records_count - 2 \
                    if records_count > 2 \
                    else 0

            if (records_count > 1 or not self.loop_enabled) and last_record_index < records_count:
                last_record = records[last_record_index]

                if self.verbose:
                    print(f"Next record : {last_record}")

                self.capture(last_record)

            elif not self.loop_enabled:
                self.stop = True

            if (not self.loop_enabled and
                    (not self.delete_record or self.check_all_records)):
                last_record_index = last_record_index + 1

        if self.show_stram:
            cv2.destroyAllWindows()

        process.terminate()

    def capture(self, last_record):
        camera_record_filename = f"{self.records_directory}/{last_record}"

        cap = cv2.VideoCapture(camera_record_filename)
        frame_rate = cap.get(5)

        while cap.isOpened() and not self.stop:
            ret, frame = cap.read()

            if ret:
                frame_id = cap.get(1)  # current frame number
                is_frame_intervale = frame_id % math.floor(frame_rate) == 0

                if is_frame_intervale:
                    frame = self.model.detect(
                        frame,
                        self.captures_directory,
                        self.save_enabled,
                        self.verbose
                    )

                    if self.show_stram:
                        cv2.imshow('Camera', frame)
            else:
                if self.verbose:
                    print(f"End record : {last_record}")

                if self.delete_record:
                    os.remove(camera_record_filename)

                break

            if self.show_stram and cv2.waitKey(1) == ord('q'):
                self.stop = True
