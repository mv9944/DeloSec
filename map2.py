import folium
import csv
import Graphics
import numpy as np
import pandas as pd
from folium import raster_layers
from PIL import Image, ImageDraw
from matplotlib.colors import LinearSegmentedColormap, rgb_to_hsv, hsv_to_rgb
import scipy.ndimage.filters

raw_data = pd.read_csv(r'C:\Users\nmega\PycharmProjects\untitled\realTimeResults\FinalResults.csv')
def get_kernel(kernel_size, blur=1 / 20, halo=.001):
    """
    Create an (n*2+1)x(n*2+1) numpy array.
    Output can be used as the kernel for convolution.
    """

    # generate x and y grids
    x, y = np.mgrid[0:kernel_size * 2 + 1, 0:kernel_size * 2 + 1]

    center = kernel_size + 1  # center pixel
    r = np.sqrt((x - center) ** 2 + (y - center) ** 2)  # distance from center

    # now compute the kernel. This function is a bit arbitrary.
    # adjust this to get the effect you want.
    kernel = np.exp(-r / kernel_size / blur) + (1 - r / r[center, 0]).clip(0) * halo
    return kernel

def add_lines(image_array, xys, width=1, weights=None):
    """
    Add a set of lines (xys) to an existing image_array
    width: width of lines
    weights: [], optional list of multipliers for lines.
    """

    for i, xy in enumerate(xys):  # loop over lines
        # create a new gray scale image
        image = Image.new("L", (image_array.shape[1], image_array.shape[0]))

        # draw the line
        ImageDraw.Draw(image).line(xy, 200, width=width)

        # convert to array
        new_image_array = np.asarray(image, dtype=np.uint8).astype(float)

        # apply weights if provided
        if weights is not None:
            new_image_array *= weights[i]

        # add to existing array
        image_array += new_image_array

    # convolve image
    new_image_array = scipy.ndimage.filters.convolve(image_array, get_kernel(width * 4))
    return new_image_array

def to_image(array, hue=.62):
    """converts an array of floats to an array of RGB values using a colormap"""

    # apply saturation function
    image_data = np.log(array + 1)

    # create colormap, change these values to adjust to look of your plot
    saturation_values = [[0, 0], [1, .68], [.78, .87], [0, 1]]
    colors = [hsv_to_rgb([hue, x, y]) for x, y in saturation_values]
    cmap = LinearSegmentedColormap.from_list("my_colormap", colors)

    # apply colormap
    out = cmap(image_data / image_data.max())

    # convert to 8-bit unsigned integer
    out = (out * 255).astype(np.uint8)
    return out

min_lat = 31.3273
max_lat = 52.2394
max_lon = 34.9385
min_lon = -97.822


def latlon_to_pixel(lat, lon, image_shape):
    # longitude to pixel conversion (fit data to image)
    delta_x = image_shape[1] / (max_lon - min_lon)

    # latitude to pixel conversion (maintain aspect ratio)
    delta_y = delta_x / np.cos(lat / 360 * np.pi * 2)
    pixel_y = (max_lat - lat) * delta_y
    pixel_x = (lon - min_lon) * delta_x
    return (pixel_y, pixel_x)

def row_to_pixel(row,image_shape):
    """
    convert a row (1 trip) to pixel coordinates
    of start and end point
    """
    start_y, start_x = latlon_to_pixel(row[0],
                                       row[1], image_shape)
    end_y, end_x = latlon_to_pixel(row[2],
                                   row[3], image_shape)
    xy = (start_x, start_y, end_x, end_y)
    return xy

image_data = np.zeros((1280,1960))

xys = row_to_pixel((31.046,34.8516,max_lat,max_lon),image_data.shape)
image_data = add_lines(image_data, xys, weights=None, width = 1)
Image.fromarray(to_image(image_data*10)[:,:,:3],mode="RGB")


def add_alpha(image_data):
    """
    Uses the Value in HSV as an alpha channel.
    This creates an image that blends nicely with a black background.
    """

    # get hsv image
    hsv = rgb_to_hsv(image_data[:, :, :3].astype(float) / 255)

    # create new image and set alpha channel
    new_image_data = np.zeros(image_data.shape)
    new_image_data[:, :, 3] = hsv[:, :, 2]

    # set value of hsv image to either 0 or 1.
    hsv[:, :, 2] = np.where(hsv[:, :, 2] > 0, 1, 0)

    # combine alpha and new rgb
    new_image_data[:, :, :3] = hsv_to_rgb(hsv)
    return new_image_data

# create the map
folium_map = folium.Map(location=[40.738, -73.98],
                        zoom_start=13,
                        tiles="CartoDB dark_matter",
                        width='100%')

# create the overlay
map_overlay = add_alpha(to_image(image_data*10))

# compute extent of image in lat/lon
aspect_ratio = map_overlay.shape[1]/map_overlay.shape[0]
delta_lat = (max_lon-min_lon)/aspect_ratio*np.cos(min_lat/360*2*np.pi)

# add the image to the map
img = raster_layers.ImageOverlay(map_overlay,
                           bounds = [(max_lat-delta_lat,min_lon),(max_lat,max_lon)],
                           opacity = 1,
                           name = "Paths")

img.add_to(folium_map)
folium.LayerControl().add_to(folium_map)

# show the map
folium_map