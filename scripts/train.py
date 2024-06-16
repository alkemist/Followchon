from ultralytics import YOLO
from datetime import datetime
import torch


def train(model_name, dataset_name, epochs=50):
    model = YOLO(f'models/{model_name}.pt')
    model.train(
        data=f'datasets/{dataset_name}/data.yaml',
        epochs=epochs,
        imgsz=1024,
        name=dataset_name,
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
        train('guinea-pig-v3+chons+camera-v5', 'camera-v6')
    except PermissionError:
        print('Permission error')

    print(f"End at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
