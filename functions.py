import numpy as np
import matplotlib.pyplot as plt
import requests
import pprint
import yaml
import cv2
from tqdm import tqdm
from io import BytesIO
from PIL import Image
import os


# Read Yaml File
with open('settings.yml', 'r') as yml:
    settings = yaml.safe_load(yml)

"""
マップの読み込み・変換を行う関数
1. load_map(Coordinates [latitude, longitude], image file name when saving, zoom:Are of map)
    return filename
    # Get and save a map image centred on the specified coordinates, scale=2, zoom=15, size=625x625, with only the roads dyed red.
    # With this setting, you get a 1250x1250px image with 2.5km square area.
    

2. map_convert(File name of the image retrieved from Google Maps, Output image name, output_image_size, scale)    
    return map, map_width, map_height
    # When input_image_size=1250x1250 and zoom=15, output_image_size=5000, scale=1 --> 1px = 50cm on Map
""" 


# Get an image from Google Map API with the roads painted red (2.5 km = 5000 px).
def load_map(filename, coordinate, zoom=15):
    # GET Parameters
    KEY = settings["Map"]["key"]
    url = settings["Map"]["url"]
    params = {"key": f"{KEY}",
              "center": f"{coordinate[0]}, {coordinate[1]}", 
              "size": "625x625",
              "scale": 2, # Get high-resolution image(1 or 2)
              "zoom": zoom, # Area of Map (1:World, 5:Landmass/continent, 10:City, 15:Streets, 20:Buildings)
              # Settings to remove informations and color roads with red
              "style": ["feature:road|color:0xff0000", "feature:administrative|visibility:off", "feature:poi|visibility:off", "feature:landscape|visibility:off", "feature:transit|visibility:off"]
              }

    # Send Request
    res = requests.get(url, params=params)

    # Extract Image Data
    img = Image.open(BytesIO(res.content))  # img is plt.image Object

    # Resize to 5000x5000px
    img.save(filename)

    return filename


# Convert Map gotton from Google Static Map API to Binary Map (Road:White, Others:Black)
def map_convert(map_image, road_image_name, output_image_size=625, scale=1):
    # make sure the scale is integer
    scale = int(scale)
    # Load Image file 
    img = cv2.imread(map_image)
    height, width = img.shape[:2]
    map_width = int(width * scale)
    map_height = int(height * scale)

    # Define Map
    map = np.zeros([map_width, map_height], dtype=np.uint8)
    # Add Road
    for x in tqdm(range(width), desc='Converting'):
        for y in range(height):
            if img[x, y, 2] == 255:  # GBR
                map[x*scale:(x+1)*scale, y*scale:(y+1)*scale] = 255    # Road:1, Wall:0
    
    # Resize Image
    map_img = Image.fromarray(map)
    up_img = map_img.resize((output_image_size, output_image_size), Image.LANCZOS)

    # Save as Image
    print(road_image_name)
    up_img.save(road_image_name)
    return map, map_width, map_height




