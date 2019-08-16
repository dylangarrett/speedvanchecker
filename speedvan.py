from xml.dom import minidom

def coordinateSplit(coords):
    ##Splits latitude and longitude
    coords = coords.split(',')
    return coords

class SpeedVanLocation(object): 
    def __init__(self, startLatLong, endLatLong, coords):
        self.startLatLong = startLatLong
        self.endLatLong = endLatLong
        self.coords = coords
        self.splitStart = coordinateSplit(startLatLong)
        self.splitEnd = coordinateSplit(endLatLong)
        # self.startLat = self.splitStart[0]
        # self.startLong = self.splitStart[1]
        # self.endLat = self.splitEnd[0]
        # self.endLong = self.splitEnd[1]

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
    # print("Start LatLong: " + elem.startLatLong)
    # print("End LatLong: " + elem.endLatLong)
    print(elem.coords)
    print("\n")

    


