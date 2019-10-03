import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def readString():
    returnLine = 0
    while 1:
        while ser.read().decode("utf-8") != '$':
            pass
        line = ser.readline().decode("utf-8")
        if line[:5] == "GPGLL":
            returnLine = line
            break

    return returnLine

def getLatLng():
    line = readString()
    lines = line.split(",")
    latString = lines[1]
    lngString = lines[3]
    lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1.0 / 60.0).lstrip("0.")
    lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1.0 / 60.0).lstrip("0.")
    return lat, lng

if __name__ == "__main__":
    latlng = getLatLng()
    print(latlng[0]+","+latlng[1])

