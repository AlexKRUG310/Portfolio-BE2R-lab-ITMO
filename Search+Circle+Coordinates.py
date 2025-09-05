import cv2 
import numpy as np

cap = cv2.VideoCapture(0) # создаем объект cap для захвата кадров

# НАСТРОЙКА ЦВЕТОВОГО ФИЛЬТРА НА ЗЕЛЁНЫЙ ЦВЕТ 
hsv_min = np.array((74, 108, 174), np.uint8) 
hsv_max = np.array((101, 168, 205), np.uint8)

color_yellow = (0,255,255)
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
while(True):
    
    flag, img = cap.read() # захватываем текущий кадр в переменную img
    
    img = cv2.flip(img,1) # отражение кадра вдоль оси Y
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV ) # ИЗМЕНЕНИЕ ЦВЕТОВОЙ МОДЕЛИ 
    thresh = cv2.inRange(hsv, hsv_min, hsv_max) # ВЫДЕЛЕНИЕ ЦВЕТОВОГО ДИАПАЗОНА

    # ВЫЧИСЛЯЕМ МОМЕНТЫ ИЗОБРАЖЕНИЯ 
    moments = cv2.moments(thresh, 1) 
    dM01 = moments['m01'] 
    dM10 = moments['m10'] 
    dArea = moments['m00']
    
    # РИСУЕМ ОКРУЖНОСТЬ В ЦЕНТРЕ ОБЪЕКТА 
    if dArea > 100: # учитыв.только моменты, содерж.> 100 пикс. 
        x = int(dM10 / dArea) 
        y = int(dM01 / dArea) 
        cv2.circle(img, (x, y), 10, (0,0,255), -1)
        cv2.putText(img, "%d-%d" % (x,y), (x-30,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

    cv2.imshow('Okno', img) # отображаем кадр в окне с именем Okno
    
    ch = cv2.waitKey(1) # выход по "Esс" (арг. - время ожидания в мс) 
    if ch == 27: 
        break

cap.release() 
cv2.destroyAllWindows()