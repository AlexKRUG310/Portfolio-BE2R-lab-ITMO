import cv2
import numpy as np

def nothing(*arg): # функция вызывается при движении бегунка 
    pass

cap = cv2.VideoCapture(1) # созд.объект cap для захвата кадров с камеры # арг.задаёт номер камеры (0 – кам.ноут.)

#Для работы с фото
#fn = 'Images\img_1.jpg' # путь к файлу с картинкой
#img = cv2.imread(fn)

cv2.namedWindow( "settings" ) # СОЗДАЁМ ОКНО ДЛЯ НАСТРОЙКИ ФИЛЬТРА

# СОЗДАЁМ 6 БЕГУНКОВ ДЛЯ НАСТРОЙКИ НАЧАЛЬНОГО И КОНЕЧНОГО ЦВЕТА ФИЛЬТРА 
cv2.createTrackbar('h1', 'settings', 0, 255, nothing) 
cv2.createTrackbar('s1', 'settings', 0, 255, nothing) 
cv2.createTrackbar('v1', 'settings', 0, 255, nothing) 
cv2.createTrackbar('h2', 'settings', 255, 255, nothing) 
cv2.createTrackbar('s2', 'settings', 255, 255, nothing) 
cv2.createTrackbar('v2', 'settings', 255, 255, nothing)

while(True): 
    flag, img = cap.read() # захв.текущ.кадр и кладем его в перем. img

    # ИЗМЕНЕНИЕ ЦВЕТОВОЙ МОДЕЛИ 
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    
    # СЧИТЫВАЕМ ЗНАЧЕННИЕ БЕГУНКОВ 
    h1 = cv2.getTrackbarPos('h1', 'settings') 
    s1 = cv2.getTrackbarPos('s1', 'settings') 
    v1 = cv2.getTrackbarPos('v1', 'settings') 
    h2 = cv2.getTrackbarPos('h2', 'settings') 
    s2 = cv2.getTrackbarPos('s2', 'settings') 
    v2 = cv2.getTrackbarPos('v2', 'settings')
    
    # ФОРМИРУЕМ НАЧАЛЬНЫЙ И КОНЕЧНЫЙ ЦВЕТ ФИЛЬТРА 
    h_min = np.array((h1, s1, v1), np.uint8) 
    h_max = np.array((h2, s2, v2), np.uint8)
    
    # НАКЛАДЫВАЕМ ФИЛЬТР НА КАДР В МОДЕЛИ HSV 
    thresh = cv2.inRange(hsv, h_min, h_max)
    
    cv2.imshow('settings', thresh) # отобр.отфильтр.кадр в окне 'settings'
    
    ch = cv2.waitKey(1) # вых.по наж."Esс" (арг.- время ожид.в мс) 
    if ch == 27: 
        break

cap.release() 
cv2.destroyAllWindows()