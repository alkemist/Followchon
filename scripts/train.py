from ultralytics import YOLO
from datetime import datetime
import torch
import os
from dotenv import load_dotenv

load_dotenv()


def train():
    model = YOLO(os.getenv('TRAIN_MODEL_PATH'))
    model.train(
        data=os.getenv('TRAIN_DATASET_PATH'),
        epochs=50,
        imgsz=1024,
        name=os.getenv('TRAIN_DATASET_NAME'),
        verbose=True,
        save=False,
        project='runs',
        exist_ok=True,
        device=0
    )


if __name__ == '__main__':
    if torch.cuda.is_available():
        print(":D GPU is available")
    else:
        print("T_T GPU is not available")

    print(f"Start at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        train()
    except PermissionError:
        print('Permission error')

    print(f"End at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
