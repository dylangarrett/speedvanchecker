from __future__ import print_function
from xml.dom import minidom
import math, time
from geopy import distance
from myGPS import getLatLng
from pygame import mixer


# Written by Dylan Garrett - hello@developerdylan.com
# www.github.com/dylangarrett

def coordinateSplit(coords):
    ##Splits latitude and longitude
    coords = coords.split(',')
    if coords == ['']:
        coords = ['0','0']    
    return coords

class myGPS(object):
    mixer.init()
    
    def __init__(self):

        self.tuple = getLatLng()
        self.lat = self.tuple[0]
        self.lng = -self.tuple[1]
        
    def update(self):
        self.tuple = getLatLng()
        self.lat = self.tuple[0]
        self.lng = -self.tuple[1]
        
    def alert(self):
        mixer.Sound("beep.wav").play()
    
    def toString(self):
        return "Latitude: " + self.lat + ", Longitude:  " + self.lng

class testGPS(object):
    mixer.init()
    
    def __init__(self):

        
        self.lat = 53.1752121
        self.lng = -6.8164815
        self.tuple = (self.lat, self.lng)
        
    def alert(self):
        mixer.Sound("beep.wav").play()
        print("Played alert sound.")
    
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
   
def scrapeData():
    mydoc = minidom.parse('xdoc.xml')
    coords = mydoc.getElementsByTagName('coordinates')

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

    del speedVanList[-1]
    del allCoords
    del coordinates

    return speedVanList

##checks the distance between the speedvans and your gps location and returns true/false depending on whether you're close to a speed van
# def distanceCheck(myGPS, speedVan):
#     closest = 500.00
#     distanceFromMidPoint = distance.distance(myGPS.tuple, speedVan.midTuple).km
#     if distanceFromMidPoint <= 3: #less than 3km
#         for coord in speedVan.coords:
#             longLat = coordinateSplit(coord)
#             coordTuple = (longLat[1], longLat[0])
#             distanceFromCoord = distance.distance(myGPS.tuple, coordTuple).km
#             if distanceFromCoord <= 0.5: #less than 300m or .3km
#                 print("Speedvan nearby at: " + coordTuple)
#                 return True
#             else:
#                 return False
#     elif distanceFromMidPoint > 3:
#         return False


def distanceFrom(GPS, speedVan):
    #print(GPS.tuple, speedVan.midTuple)
    distanceFrom = distance.distance(GPS.tuple, speedVan.midTuple).km
    return distanceFrom

def distanceCheck(myGPS, speedVanList):
    closest = 500.00
    for speedvan in speedVanList:   
        if distanceFrom(GPS, speedvan) < closest:
            closest = distanceFrom(GPS, speedvan)
    distanceKM = str(closest)
    print("Closest speedvan is " + distanceKM + "km away")
    if closest < 0.8:
        print("Speedvan nearby!")
        myGPS.alert()

if __name__ == '__main__':

    speedVanList = scrapeData()
    GPS = myGPS()
    run = True

    print("Running")
    while(run):
        GPS.update()
        print(GPS.toString())
        distanceCheck(GPS, speedVanList)
        time.sleep(3)


    


