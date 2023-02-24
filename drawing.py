import sys
from PIL import Image, ImageDraw
import json


with open('json-files/571673-FP-B7R1-MB9F.json') as order_json_file:
    json_data = json.load(order_json_file)
    stones = json_data['profile']['stoneLayout']

# print(stones)
# print(len(stones))
# print(stones[0]['placements'])
list_of_coordinates = []
list_of_dicts = stones[0]['placements']
for coordinates_dict in list_of_dicts:
    # list_of_coordinates.append((coordinates_dict.ke))
    list_of_coordinates.append((coordinates_dict.get('x'), coordinates_dict.get('y')))

coords_dict = {}
for i, x in enumerate(list_of_coordinates):
    first_point = ((x[0]+1)*-50, (x[1]+1)*50, (x[0]-1)*-50, (x[1]-1)*50)
    # second_point = (, )
    coords_dict[i+1] = first_point

# print(list_of_coordinates)
# print(coords_dict)
print(coords_dict)

width = 400
height = 800

img = Image.new(mode='RGB', size=(width, height), )
draw = ImageDraw.Draw(img)
for y in coords_dict.values():
    draw.ellipse(y, fill='blue')

# draw.ellipse((20,20,180,180), fill='blue')

img = img.save('test.jpg')
