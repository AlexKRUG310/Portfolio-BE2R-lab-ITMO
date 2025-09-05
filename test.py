from WGS_Kruger_def import WGS_KRUGER, WGS_KRUGER_BACK
from target_coordinates import target_coordinates

lat, lon = 60.0561, 30.4319

Xbpla, Ybpla = WGS_KRUGER(60.0561, 30.4319)

print(Xbpla, Ybpla)

tc = target_coordinates(30, 10, 10, 32, 32, 720, 1080, 820, 400, Xbpla, Ybpla)

X, Y = tc.get_coordinates()
print(X, Y)

lon_back, lat_back  = WGS_KRUGER_BACK(lat, lon, X, Y)

print(lat_back, lon_back)