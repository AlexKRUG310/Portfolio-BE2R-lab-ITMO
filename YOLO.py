import torch
torch.cuda.empty_cache()

from ultralytics import YOLO

model = YOLO("yolo12n.pt")
if __name__ == '__main__':
    result = model.train(data='C:/Users/krugl/Desktop/YOLO/datasets/my_dataset_yolo/data.yaml',epochs = 100, batch=5, imgsz=640)

