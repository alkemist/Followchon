# venv/bin/python -m src.vision
import os

from .models.streamer import Streamer
from dotenv import load_dotenv

load_dotenv()

check_all_records = os.getenv('check_all_records') == 'True'
verbose = os.getenv('verbose') == 'True'
save_enabled = os.getenv('save_enabled') == 'True'
loop_enabled = os.getenv('loop_enabled') == 'True'
delete_record = os.getenv('delete_record') == 'True'
show_stream = os.getenv('show_stream') == 'True'

streamer = Streamer(
    os.getenv('LIVE_STREAM_PATH'),
    os.getenv('MODEL_PATH'),
    './live/records',
    './live/captures',
    capture_width=1024,
    capture_height=768,
    check_all_records=check_all_records,
    show_stream=show_stream,
    verbose=verbose,
    save_enabled=save_enabled,
    loop_enabled=loop_enabled,
    delete_record=delete_record,
)

streamer.start()
