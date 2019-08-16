from xml.dom import minidom
import math

def coordinateSplit(coords):
    ##Splits latitude and longitude
    coords = coords.split(',')
    if coords == ['']:
        coords = ['0','0']
    return coords

def myGPS(object):

    def __init__(self, lat, long):
        self.lat = lat
        self.long = long



class SpeedVanLocation(object): 

    def __init__(self, startLatLong, endLatLong, coords):
        self.startLatLong = startLatLong
        self.endLatLong = endLatLong
        self.coords = coords
        self.splitStart = coordinateSplit(startLatLong)
        self.splitEnd = coordinateSplit(endLatLong)
        self.startLat = self.splitStart[1]
        self.startLong = self.splitStart[0]
        self.endLat = self.splitEnd[1]
        self.endLong = self.splitEnd[0]

    def midPoint(self):

        ##since the coordinates are so close you can take them as two points on a plan

        lat1 = float(self.startLat)
        lat2 = float(self.endLat)
        long1 = float(self.startLong)
        long2 = float(self.endLong)

        midLat = (lat1 + lat2)/2
        midLong = (long1 + long2)/2

        midPoint = []
        midPoint.append(midLat)
        midPoint.append(midLong)
        return midPoint

        ##cartesian values for calculating mid point
        

##FIRST STEP
##Clean up the data from the .kmz file
##Convert from .kmz to .kml to .xml

print("Opening document..")
mydoc = minidom.parse('xdoc.xml')
print("Document opened.")

print("Scraping document..")
coords = mydoc.getElementsByTagName('coordinates')
print("Document scraped.")

print("Initializing allCoords list..")
allCoords = ''
print("List initialized.")

print("Passing data from document in to allCoords list..")
for elem in coords:
    allCoords = allCoords + elem.firstChild.data.replace(",0.0", "") + "/n"
print("Success.")

print("Splitting allCoords..")
coordinates = allCoords.split("/n")
print("Split successful.")

print("Cleaning up list, making list of lists..")
coordinates = [i.split(' ') for i in coordinates]
print("Success.")


#list of speedVanLocation objects
speedVanList = []


for elem in coordinates:
    lastVal = len(elem) - 1    
    speedVanList.append(SpeedVanLocation(elem[0], elem[lastVal], elem))

del speedVanList[-1]

for elem in speedVanList:
    print("Start Lat: " + elem.startLat + " - Start Long: " + elem.startLong)
    print("End Lat: " + elem.endLat + " - End Long: " + elem.endLong)
    midPoint = elem.midPoint()
    print(midPoint)
    print("\n")

   

##find the middle point of the coordinates
##draw circle around the coordinates (radius)
##if my gps coordinates are within that circle
##draw smaller circles around the coordinates between first and last point
##if my gps coordinates are within any of the smaller circles
##beep beep beep

    


