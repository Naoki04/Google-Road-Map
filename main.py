import numpy as np
import matplotlib.pyplot as plt
import requests
import pprint
import yaml
import cv2
from tqdm import tqdm
import csv
from io import BytesIO
from PIL import Image
# import functions
from functions import load_map, map_convert


# Read yaml
with open('settings.yml', 'r') as yml:
    settings = yaml.safe_load(yml)


# /** Parameters **/
coordinate = [35.0469245, 135.7464617] # Coordinate of Map Center (Shinomiya Arcade in Japan)
zoom = 15 # Area of Map (1:World, 5:Landmass/continent, 10:City, 15:Streets, 20:Buildings)
output_image_size = 5000 # resize to 5000x5000px

loaded_image_name = "output/road_river.png"  # File name of saved map image with rivers and roads
road_image_name = "output/road.png"  # File name of saved map image with rivers and roads


def main():
    # Get Map including River and Road from Google Map API
    load_map(loaded_image_name, coordinate, zoom)
    print("Map :" + loaded_image_name + " is Downloaded")

    # Convert Map to Binary Map (Road:White, Others:Black)
    map, width, height = map_convert(loaded_image_name, road_image_name, output_image_size=5000, scale=1)  #image, scale
    print("width:height = " + str(width) + " : " + str(height))

    # Show Map
    print("Saving converted map as an image......", end="")
    plt.imshow(map, cmap='gist_gray', interpolation='nearest')
    plt.show()


if __name__ == '__main__':
    main()