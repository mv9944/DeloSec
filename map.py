import folium
import csv
import Graphics
import numpy as np
import pandas as pd
from folium import raster_layers
from PIL import Image, ImageDraw

masterLat = float(31.046)
masterLon = float(34.8516)
max_lon = 0
max_lat = 0

raw_data = pd.read_csv(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\FinalResults.csv')
cordinates = [["Start Station Latitude", "Start Station Longitude", "End Station Latitude", "End Station Longitude"]]

min_lat = masterLat
min_lon = masterLon

#pt_lyr = folium.FeatureGroup(name = 'pt_lyr')


folium_map = folium.Map(zoom_start=13, tiles="CartoDB dark_matter", width='100%')
marker = folium.CircleMarker(location=[masterLat, masterLon])
marker.add_to(folium_map)

folium.LayerControl().add_to(folium_map)
def add2Map(lon,lat):
    #print(lon,lat)
    popup_text = 'Amazing'
    marker = folium.CircleMarker(location=[lon,lat],popup=popup_text)
    marker.add_to(folium_map)
    appendix = [float(lat),float(lon),float(masterLat),float(masterLon)]
    # print(appendix)
    cordinates.append(appendix)

def get_arrows(locations, color='red', size=9, n_arrows=3):
    '''
    Get a list of correctly placed and rotated
    arrows/markers to be plotted

    Parameters
    locations : list of lists of lat lons that represent the
                start and end of the line.
                eg [[41.1132, -96.1993],[41.3810, -95.8021]]
    arrow_color : default is 'blue'
    size : default is 6
    n_arrows : number of arrows to create.  default is 3
    Return
    list of arrows/markers
    '''


    # creating point from our Point named tuple
    p1 = (locations[0][0], locations[0][1])
    p2 = (locations[1][0], locations[1][1])
    #print("Here 4   " , p1[1], "   ", p2[0])

    # getting the rotation needed for our marker.
    # Subtracting 90 to account for the marker's orientation
    # of due East(get_bearing returns North)
    #rotation = get_bearing(p1, p2) - 90

    # get an evenly space list of lats and lons for our arrows
    # note that I'm discarding the first and last for aesthetics
    # as I'm using markers to denote the start and end
    arrow_lats = np.linspace(p1[0], p2[0], n_arrows + 2)[1:n_arrows + 1]
    arrow_lons = np.linspace(p1[1], p2[1], n_arrows + 2)[1:n_arrows + 1]

    arrows = []

    # creating each "arrow" and appending them to our arrows list
    for points in zip(arrow_lats, arrow_lons):
        arrows.append(folium.RegularPolygonMarker(location=points,
                                                  fill_color=color, number_of_sides=3,
                                                  radius=size).add_to(folium_map))
    return arrows

def get_bearing(p1, p2):
    '''
    Returns compass bearing from p1 to p2

    Parameters
    p1 : namedtuple with lat lon
    p2 : namedtuple with lat lon

    Return
    compass bearing of type float

    Notes
    Based on https://gist.github.com/jeromer/2005586
    '''

    long_diff = np.radians(p2[1] - p1[1])

    lat1 = np.radians(p1[0])
    lat2 = np.radians(p2[0])

    x = np.sin(long_diff) * np.cos(lat2)
    y = (np.cos(lat1) * np.sin(lat2)
         - (np.sin(lat1) * np.cos(lat2)
            * np.cos(long_diff)))
    bearing = np.degrees(np.arctan2(x, y))

    # adjusting for compass bearing
    if bearing < 0:
        return bearing + 360
    return bearing

def corIter ():

    i = 0
    temp = 0
    for row in cordinates:
        if (i != 0):
            #print(temp[1])
            Graphics.setMaxLat(row[2])
            Graphics.setMaxLon(row[3])
            p1 = [masterLat,masterLon]
            p2 = [row[1],row[0]]
            folium.PolyLine(locations=[p2, p1], color='blue').add_to(folium_map)
            arrows = get_arrows(locations=[p2, p1], n_arrows=6)
            #print(row)
        i += 1

    print("out ")
    print(temp)


def add2Line(lon,lat):
    image_data = np.zeros((900, 400))
    # image_data = Graphics.add_lines(image_data, xys, weights=None, width=1)
    # Image.fromarray(Graphics.to_image(image_data * 10)[:, :, :3], mode="RGB")
    # img = raster_layers.ImageOverlay(map_overlay,
    #                                  bounds=[(max_lat - delta_lat, min_lon), (max_lat, max_lon)],
    #                                  opacity=1,
    #                                  name=cordinates)
    # img.add_to(folium_map)
    # folium.LayerControl().add_to(folium_map)
    # print(xys)
    row = [int(min_lat),int(min_lon),int(lat),int(lon)]
    print (row)
    xys = [Graphics.row_to_pixel(row,image_data.shape)]
    print("here 2")

with open(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\FinalResults.csv') as csvfile:
    ff = reader = csv.DictReader(csvfile)
    for row in ff:
     try:
         Longitude =float(row['Latitude'])
         Latitude = float(row['Longitude'])
         add2Map(Longitude,Latitude)
     except Exception as e:
         print(e)

corIter()
#folium_map.add_child(pt_lyr)

print("f")

folium_map.zoom_start = 3
folium_map.save("my_map.html")


