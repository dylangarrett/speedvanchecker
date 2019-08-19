from xml.dom import minidom
import math
from geopy import distance

# Written by Dylan Garrett - dylan@webfire.co
# 19/08/2018

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

##triggers if you are close to a speed van
def alert():
     #method to alert the driver
     #play sound/flash light etc;
     #prints beep for now
     print("BEEP BEEP BEEP")
     return "BEEP BEEP BEEP"

##takes the data from the .xml file and returns a list filled with 'clean'ish data
def scrapeData():

    #open the document
    mydoc = minidom.parse('xdoc.xml')

    #scrape the coordinates from the document
    coords = mydoc.getElementsByTagName('coordinates')

    #create a list for all the coordinates
    allCoords = ""

    #cleans and passes data from the document into the list
    for elem in coords:
        allCoords = allCoords + elem.firstChild.data.replace(",0.0", "") + "/n"

    #split the coordinates, creating a list of lists
    #the first element is a list of all coordinates associated with a speed van
    coordinates = allCoords.split("/n")
    coordinates = [i.split(' ') for i in coordinates]

    #creates list of speedvanlocation objects using the data from the previous list
    speedVanList = []
    for elem in coordinates:
        lastVal = len(elem) - 1    
        speedVanList.append(SpeedVanLocation(elem[0], elem[lastVal], elem))

    ##removing invalid values and unnecessary lists
    del speedVanList[-1]
    del allCoords
    del coordinates

    return speedVanList

##checks the distance between the speedvans and your gps location and returns true/false depending on whether you're close to a speed van
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
    # run = True

    # while(run):
        #print("Running")
        #update gps location
        # gpsLat = 1  #pass in value from gps
        # gpsLong = 2 #pass in value from gps
        # GPS = myGPS(55.139766, -8.228917) #replace values with gpslat and gpslong
    
        # for speedVan in speedVanList:
        #     if(distanceCheck(GPS, speedVan)):
        #         alert()

    testString = ''
    print("Testing coordinate which should trigger alert..")
    GPS = myGPS(55.139766, -8.228917)
    for speedVan in speedVanList:
        if(distanceCheck(GPS, speedVan)):
            testString += alert()
            break

    print("Testing coordinate which should not trigger alert..")
    GPS = myGPS(59.139766, -8.228917)
    for speedVan in speedVanList:
        if(distanceCheck(GPS, speedVan)):
            testString += alert()
            break
    
    if(testString == 'BEEP BEEP BEEP'):
        print("Test successful. Conditions passed.")

main()
    


