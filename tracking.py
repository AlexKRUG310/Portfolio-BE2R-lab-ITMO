# -*- coding: utf-8 -*-
import cv2
from ultralytics import YOLO
import numpy as np
from WGS_Kruger import WGS_KRUGER, WGS_KRUGER_BACK
from get_coordinates import get_coordinates


#НАСТРОЙКА ЦВЕТОВОГО ФИЛЬТРА
hsv_min = np.array((0, 150, 56), np.uint8) 
hsv_max = np.array((7, 156, 72), np.uint8)

#Цвет для YOLO
yolo_color = (0, 255, 0)

#Цвет для фильтра
filter_color = (0, 0, 255)

def process_video_with_tracking(model, input_video_path, show_video=True, YOLO = False, Filter = True, save_video=True, output_video_path = "Experiment_filter_out.mp4" ):
    # Открываем видео файл
    cap = cv2.VideoCapture(input_video_path)
    
    # Получаем количество кадров в секунду и размер видео
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Определение выходного файла
    if save_video:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))


      
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        #blured_frame = cv2.GaussianBlur(frame, (5, 5), sigmaX=0)
        #Широта и долгота БПЛА
        lat, lon = 60.05474, 30.431816

        #Получение прямоугольных координат
        Xbpla, Ybpla = WGS_KRUGER(lat, lon)

      #--------------------------------#
        #Детектирование с помощью YOLO
      #--------------------------------#
        if YOLO == True:
            results = model.track(frame, iou=0.4, conf=0.3, persist=True, imgsz=608, verbose=False, tracker="bytetrack.yaml")
    
            if results[0].boxes.id != None: # если модель обнаружила объект
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                ids = results[0].boxes.id.cpu().numpy().astype(int)
    
                for box, id in zip(boxes, ids):
                    
                    
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), yolo_color, 2)
                    #cv2.putText(frame, f"Id {id}", (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2,)
                    
                    Xp = int((box[2] + box[0])/2)
                    Yp = int((box[3] + box[1])/2)
                    
                    
                    X, Y = get_coordinates(-90, 50, 23.4, 56, 34, 720, 1280, Xp, Yp, Xbpla, Ybpla)
    
                    lon_back, lat_back  = WGS_KRUGER_BACK(lat, lon, X, Y)
                    
                    if Xp < 1080/2:
                        cv2.putText(frame, "lat-lon: "+"%.6f-%.6f" % (lat_back,lon_back), (Xp + 20, Yp - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, yolo_color, 2)
                    
                    else: 
                        cv2.putText(frame, "lat-lon: "+"%.6f-%.6f" % (lat_back,lon_back), (Xp - 400, Yp - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, yolo_color, 2)
    #--------------------------------#
        #Обнаружение по цвету
    #--------------------------------#
        if Filter == True:            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV ) # ИЗМЕНЕНИЕ ЦВЕТОВОЙ МОДЕЛИ 
            thresh = cv2.inRange(hsv, hsv_min, hsv_max) # ВЫДЕЛЕНИЕ ЦВЕТОВОГО ДИАПАЗОН
            
            # ВЫЧИСЛЯЕМ МОМЕНТЫ ИЗОБРАЖЕНИЯ 
            moments = cv2.moments(thresh, 1) 
            dM01 = moments['m01'] 
            dM10 = moments['m10'] 
            dArea = moments['m00']
            
            # РИСУЕМ ОКРУЖНОСТЬ В ЦЕНТРЕ ОБЪЕКТА
            if dArea > 100: # учитыв.только моменты, содерж.> 100 пикс. 
                Xc = int(dM10 / dArea) 
                Yc = int(dM01 / dArea) 
                cv2.circle(frame, (Xc, Yc), 10, (0,0,255), -1)
                
                X_c, Y_c = get_coordinates(30, 10, 10, 32, 32, 720, 1080, Xc, Yc, Xbpla, Ybpla)
                lon_back_c, lat_back_c  = WGS_KRUGER_BACK(lat, lon, X_c, Y_c)
                cv2.putText(frame, "lat-lon: "+"%.6f-%.6f" % (lat_back_c,lon_back_c), (Xc + 20, Yc - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, filter_color, 2)
        
        if save_video:
            out.write(frame)
        
        if show_video:
            frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
            cv2.imshow("frame", frame)
            #cv2.imshow("blured_frame", blured_frame)

        ch = cv2.waitKey(1) # вых.по наж."Esс" (арг.- время ожид.в мс) 
        if ch == 27: 
            break

    # Release the input video capture and output video writer,
    cap.release()

    # Закрытие окон
    cv2.destroyAllWindows()


model = YOLO('runs/detect/train/weights/best.pt')
model.fuse()
process_video_with_tracking(model, "Experiment_long.mp4", show_video=True, YOLO=1, Filter=0, save_video=1, output_video_path="Experiment_long_YOLO_out.mp4")
