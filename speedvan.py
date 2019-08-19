from xml.dom import minidom
import math
from geopy import distance
import time

def coordinateSplit(coords):
    ##Splits latitude and longitude
    coords = coords.split(',')
    if coords == ['']:
        coords = ['0','0']
    return coords

class myGPS(object):

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.tuple = (lat, lon)

class SpeedVanLocation(object): 

    def midPoint(self):
        ##since the coordinates are so close you can take them as two points on a plane
        lat1 = float(self.startLat)
        lat2 = float(self.endLat)
        long1 = float(self.startLong)
        long2 = float(self.endLong)

        midLat = (lat1 + lat2)/2
        midLong = (long1 + long2)/2

        midTuple = (midLat, midLong)
        return midTuple

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
        self.startTuple = (self.startLat, self.startLong)
        self.endTuple = (self.endLat, self.endLong)
        self.midTuple = self.midPoint()

def alert():
     #method to alert the driver
     #play sound/flash light etc;
     #prints beep for now
     print("BEEP BEEP BEEP")

def scrapeData():

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

    speedVanList = []

    for elem in coordinates:
        lastVal = len(elem) - 1    
        speedVanList.append(SpeedVanLocation(elem[0], elem[lastVal], elem))

    del speedVanList[-1]

    return speedVanList

def distanceCheck(myGPS, speedVan):
    ##both inputs should be in format tuple (lat,lon)
    distanceFromMidPoint = distance.distance(myGPS.tuple, speedVan.midTuple).km
    if distanceFromMidPoint <= 3:
        for coord in speedVan.coords:
            longLat = coordinateSplit(coord)
            coordTuple = (longLat[1], longLat[0])
            distanceFromCoord = distance.distance(myGPS.tuple, coordTuple).km
            if distanceFromCoord <= 0.5:
                return True
            else:
                return False
    elif distanceFromMidPoint > 3:
        return False

def main():

    speedVanList = scrapeData()

    print("Setting run = true")
    run = True

    # while(run):
        #print("Running")
        #update gps location
        # gpsLat = 1  #pass in value from gps
        # gpsLong = 2 #pass in value from gps
        # GPS = myGPS(55.139766, -8.228917) #replace values with gpslat and gpslong
    
        # for speedVan in speedVanList:
        #     if(distanceCheck(GPS, speedVan)):
        #         alert()

    GPS = myGPS(55.139766, -8.228917)
    for speedVan in speedVanList:
        if(distanceCheck(GPS, speedVan)):
            alert()

main()
    


