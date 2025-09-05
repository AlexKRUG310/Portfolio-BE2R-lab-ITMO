import cv2
import numpy as np

def nothing(*arg): # функция вызывается при движении бегунка 
    pass

image = cv2.imread("Exmpl_sun.png")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)



cv2.namedWindow( "settings" ) # СОЗДАЁМ ОКНО ДЛЯ НАСТРОЙКИ ФИЛЬТРА

# СОЗДАЁМ 6 БЕГУНКОВ ДЛЯ НАСТРОЙКИ НАЧАЛЬНОГО И КОНЕЧНОГО ЦВЕТА ФИЛЬТРА 
cv2.createTrackbar('h1', 'settings', 0, 255, nothing) 
cv2.createTrackbar('s1', 'settings', 0, 255, nothing) 
cv2.createTrackbar('v1', 'settings', 0, 255, nothing) 
cv2.createTrackbar('h2', 'settings', 255, 255, nothing) 
cv2.createTrackbar('s2', 'settings', 255, 255, nothing) 
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)

color = (13, 234, 2)

mark = 0 # 1 - поиск, 0 - настройка
while(True):
    
    cv2.imshow("RGB",image)
    #cv2.imshow("HSV",hsv)
    
    
    h1 = cv2.getTrackbarPos('h1', 'settings') 
    s1 = cv2.getTrackbarPos('s1', 'settings') 
    v1 = cv2.getTrackbarPos('v1', 'settings') 
    h2 = cv2.getTrackbarPos('h2', 'settings') 
    s2 = cv2.getTrackbarPos('s2', 'settings') 
    v2 = cv2.getTrackbarPos('v2', 'settings')
    
    if mark == 1:
        #Для поиска
        h_min = np.array((0, 150, 56), np.uint8) 
        h_max = np.array((7, 156, 72), np.uint8)
    
    else:
        #Для настройки фильтра
        h_min = np.array((h1, s1, v1), np.uint8) 
        h_max = np.array((h2, s2, v2), np.uint8)
    
    # НАКЛАДЫВАЕМ ФИЛЬТР НА КАДР В МОДЕЛИ HSV 
    thresh = cv2.inRange(hsv, h_min, h_max)
    
    cv2.imshow('settings', thresh)
    
    moments = cv2.moments(thresh, 1) 
    dM01 = moments['m01'] 
    dM10 = moments['m10'] 
    dArea = moments['m00']
    
    if dArea > 0: # учитыв.только моменты, содерж.> 100 пикс. 
        Xc = int(dM10 / dArea) 
        Yc = int(dM01 / dArea) 
        cv2.circle(image, (Xc, Yc), 10, (0,0,255), -1)
        cv2.putText(image, "X-Y: "+"%.0f-%.0f" % (Xc,Yc), (Xc - 150, Yc - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
     
    
    ch = cv2.waitKey(1) # вых.по наж."Esс" (арг.- время ожид.в мс) 
    if ch == 27: 
        break
    
cv2.destroyAllWindows()