# -*- coding: utf-8 -*-
from math import sin, cos, tan, radians
from mpmath import cot

class target_coordinates():
    
    def __init__(self, az, pich, high, hv, vv, Py, Px, Xp, Yp, Xbpla, Ybpla):
        self.az = radians(az) # азимут
        self.pitch = radians(pich) # угол тангажа
        self.high = high # высота
        self.hv = radians(hv) #угол обзора по горизонтали 
        self.vv = radians(vv) #уггол обзора по вертикали
        self.Py = Py #количество пикселей по вертикали
        self.Px = Px #количество пикселей по горизонтали
        self.Xp = Xp #координата цели по горизонтали в пикселях
        self.Yp = Yp #координата цели по вертикали в пикселях
        self.a = self.high * tan(pich) # расстояние от БПЛА до площади, покрываемой камерой
        self.b = self.a - tan(pich + vv) * self.high #вертикальное расстояние в м
        self.c = 2 * self.a / cot(hv/2) #горизонтальное расстояние в м
        self.Xbpla = Xbpla #Прямоугльные координаты БПЛА
        self.Ybpla = Ybpla
        
    def get_coordinates(self):
        # количество метров в 1 пикселе
        Mx = self.c / self.Px 
        My = self.b / self.Py
        
        #расстояние в метрах до цели от верхнего левого угла кадра
        Xpm = self.Xp * Mx
        Ypm = self.Yp * My
        
        #цель в первой четверти (ось координат, привязанная к направлению полёта бпла)
        if Xpm < self.c / 2 :
            
            if self.az < 90 and self.az > 0:
                
                Xt = (self.a + self.b - (self.c/2 - Xpm) / tan(self.az) - Ypm) * sin(self.az) #Координаты относительно БПЛА 
                Yt = Xt / tan(self.az) + (self.c/2 - Xpm) / sin(self.az)
                
                X = self.Xbpla + Xt #Прямоугольные координаты 
                Y = self.Ybpla + Yt
            
            if self.az < 0 and self.az > -90:
                
                Xt = (self.b + self.a - tan(self.az) *(self.c/2 - Xpm) - Ypm) * sin(self.az) + (tan(self.az) * (self.c/2 - Xpm))/sin(self.az) 
                Yt = (self.b + self.a - tan(self.az) *(self.c/2 - Xpm) - Ypm) * cos(self.az)
                
                X = self.Xbpla - Xt 
                Y = self.Ybpla + Yt
                
                
            if self.az < 180 and self.az > 90:
                
                Yt = (self.a + self.b - (self.c/2 - Xpm) / tan(self.az - radians(90)) - Ypm) * sin(self.az - radians(90))
                Xt = Yt / tan(self.az - radians(90)) + (self.c/2 - Xpm) / sin(self.az - radians(90))
                
                X = self.Xbpla + Xt 
                Y = self.Ybpla - Yt
                
            if self.az < 270 and self.az > 180:
                
                Xt = (self.b + self.a - tan(radians(270) - self.az) * (self.c/2 - Xpm) - Ypm) * cos(radians(270) - self.az)
                Yt = (self.b + self.a - tan(radians(270) - self.az) * (self.c/2 - Xpm) - Ypm) * sin(radians(270) - self.az) + tan((radians(270) - self.az) * (self.c/2 - Xpm))/sin(radians(270) - self.az)
                
                X = self.Xbpla - Xt
                Y = self.Ybpla - Yt
                
            
                
        #цель в четвёртой четверти (ось координат, привязанная к направлению полёта бпла)        
        else:
             
            if self.az < 90 and self.az > 0:
                 
                 Xt = (self.b + self.a - tan(self.az) *(Xpm - self.c/2) - Ypm) * sin(self.az) + (tan(self.az) * (Xpm - self.c/2))/sin(self.az) 
                 Yt = (self.b + self.a - tan(self.az) *(Xpm - self.c/2) - Ypm) * cos(self.az)
                 
                 X = self.Xbpla + Xt #Прямоугольные координаты 
                 Y = self.Ybpla + Yt
             
            if self.az < 0 and self.az > -90:
                 
                 Xt = (self.a + self.b - (Xpm - self.c/2) / tan(self.az) - Ypm) * sin(self.az) 
                 Yt = Xt / tan(self.az) + (Xpm - self.c/2) / sin(self.az)
                 
                 X = self.Xbpla - Xt 
                 Y = self.Ybpla + Yt
                 
                 
            if self.az < 180 and self.az > 90:
                 
                 Yt = (self.b + self.a - tan(radians(270) - self.az) * (Xpm - self.c/2) - Ypm) * cos(radians(270) - self.az)
                 Yt = (self.b + self.a - tan(radians(270) - self.az) * (Xpm - self.c/2) - Ypm) * sin(radians(270) - self.az) + tan((radians(270) - self.az) * (Xpm - self.c/2))/sin(radians(270) - self.az)
                 
                 X = self.Xbpla + Xt 
                 Y = self.Ybpla - Yt
                 
            if self.az < 270 and self.az > 180:
                 
                 Xt = (self.a + self.b - (Xpm - self.c/2) / tan(self.az - radians(90)) - Ypm) * sin(self.az - radians(90))
                 Xt = Yt / tan(self.az - radians(90)) + (Xpm - self.c/2) / sin(self.az - radians(90))
                 
                 X = self.Xbpla - Xt
                 Y = self.Ybpla - Yt
                 
        return X, Y