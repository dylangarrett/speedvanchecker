import time 
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def readString():
    while 1:
        while ser.read().decode("utf-8") != '$':  # Wait for the start of string
            pass  # Do nothing
        line = ser.readline().decode("utf-8")  # Read the entire string
        return line


def getTime(string, format, returnFormat):
    return time.strftime(returnFormat,
                         time.strptime(string, format))  # Convert date and time to a nice printable format


def getLatLng(latString, lngString):
    lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1.0 / 60.0).lstrip("0.")
    lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1.0 / 60.0).lstrip("0.")
    return lat, lng

def printGLL(lines):
    print("=====GLL=====")
    # print(lines, '\n')
    latlng = getLatLng(lines[1], lines[3])
    print("Lat,Long: ", latlng[0], lines[2], ", ", latlng[1], lines[4], sep='')
    print("Fix taken at:", getTime(lines[5], "%H%M%S.%f", "%H:%M:%S"), "UTC")

def liveLatLong():
    line = readString()
    lines = line.split(",")
    latlng = getLatLng(lines[1], lines[3])
    return latlng

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Open Serial port
    try:
        while True:
            line = readString()
            lines = line.split(",")
            if lines[0] == "GPGLL":
                #printGLL(lines)
                latLongTuple(lines)
                pass

    except KeyboardInterrupt:
        print('Exiting Script')
