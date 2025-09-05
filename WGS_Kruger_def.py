from pyproj import Transformer, CRS

#Transformer — класс для преобразования координат между разными системами
#CRS (Coordinate Reference System) — класс для работы с системами координат

# КООРДИНАТЫ ДРОНА (ШИРОТА, ДОЛГОТА)

def WGS_KRUGER (lat, lon):
    # 1. Определяем номер зоны Гаусса-Крюгера (6° зоны)(ФОРМУЛЫ ИЗ ГЕОДЕЗИИ)
    zone = int((lon + 6) // 6)
    central_meridian = zone * 6 - 3  # Осевой меридиан зоны
    false_easting = zone * 1_000_000 + 500_000  # Смещение по X (ДЛЯ ТОГО, ЧТОБЫ КООРДИНАТЫ НЕ БЫЛИ ОТРИЦАТЕЛЬНЫМИ)
    
    # 2. Создаём CRS для WGS84 и Гаусса-Крюгера
    crs_wgs84 = CRS.from_epsg(4326)  # WGS84 (широта/долгота)
    crs_gk = CRS(
        proj="tmerc",          # Поперечная проекция Меркатора
        lat_0=0,               # Начальная широта (экватор)
        lon_0=central_meridian, # Осевой меридиан зоны (39° для зоны 7)
        k=1,                   # Масштабный коэффициент
        x_0=false_easting,     # Смещение по X (7_500_000 для зоны 7)
        y_0=0,                 # Смещение по Y
        ellps="krass",         # Эллипсоид Красовского (для СК-95)
        units="m",             # Метры
    )
    
    # 3. Преобразование
    transformer = Transformer.from_crs(crs_wgs84, crs_gk, always_xy=True)
    Xbpla, Ybpla = transformer.transform(lon, lat)  # Обратить внимание: (lon, lat)
    
    return Xbpla, Ybpla

def WGS_KRUGER_BACK (lat, lon, X, Y):
    zone = int((lon + 6) // 6)
    central_meridian = zone * 6 - 3  # Осевой меридиан зоны
    false_easting = zone * 1_000_000 + 500_000
    
    crs_wgs84 = CRS.from_epsg(4326)  # WGS84 (широта/долгота)
    crs_gk = CRS(
        proj="tmerc",          # Поперечная проекция Меркатора
        lat_0=0,               # Начальная широта (экватор)
        lon_0=central_meridian, # Осевой меридиан зоны (39° для зоны 7)
        k=1,                   # Масштабный коэффициент
        x_0=false_easting,     # Смещение по X (7_500_000 для зоны 7)
        y_0=0,                 # Смещение по Y
        ellps="krass",         # Эллипсоид Красовского (для СК-95)
        units="m",             # Метры
    )
    transformer_back = Transformer.from_crs(crs_gk, crs_wgs84, always_xy=True)
    lon_back, lat_back   = transformer_back.transform(X, Y)
    
    return lon_back, lat_back

