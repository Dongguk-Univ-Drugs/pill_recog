from PIL import Image
import os

target_path = "test_images"
origin_path = "origin_images"
type_coordinates = [(34, 73, 1213, 549),(54,0,780,333),(20,43,729,388)]

def make_test_images(type_number, coordinates):
    image_path = f"{origin_path}/type{type_number}"
    file_list = [f for f in os.listdir(image_path) if f.endswith('png')]
    for file in file_list:
        image = Image.open(f"{image_path}/{file}")
        width, height = image.size
        cropped_image = image.crop(coordinates)
        cropped_width, cropped_height = cropped_image.size
        left_cropped_image = cropped_image.crop((0, 0, cropped_width/2, cropped_height))
        rigth_cropped_image = cropped_image.crop((cropped_width/2, 0, cropped_width, cropped_height))

        title, tail = file.split('.')
        left_cropped_image.save(f'{target_path}/{title}_l.{tail}')
        rigth_cropped_image.save(f'{target_path}/{title}_r.{tail}')

""" config
    type1 => file : 196200046.png, coordinates : (34, 73, 1213, 549), size : (1299, 709)
    type2 => file : 198200131.png, coordinates : (34, 73, 1213, 549), size : (780, 426)
    type3 => file : 198400322.png, coordinates : (34, 73, 1213, 549), size : (780, 426)
"""

""" test code """

# test_files = ["196200046", "198200131", "198400322"]
# for type_number, file in enumerate(test_files): 
#     image = Image.open(f"{file}.png")
#     width, height = image.size
#     print(f"{file} : {width}, {height}")
#     cropped_image = image.crop(type_coordinates[type_number])
#     cropped_width, cropped_height = cropped_image.size
#     if type_number == 1:
#         left_cropped_image = cropped_image.crop((0, 0, cropped_width, cropped_height/2))
#         rigth_cropped_image = cropped_image.crop((0, cropped_height/2, cropped_width, cropped_height))
#     else:
#         left_cropped_image = cropped_image.crop((0, 0, cropped_width/2, cropped_height))
#         rigth_cropped_image = cropped_image.crop((cropped_width/2, 0, cropped_width, cropped_height))
#     left_cropped_image.save(f'{file}_cropped_left.png')
#     rigth_cropped_image.save(f'{file}_cropped_right.png')

make_test_images(1, type_coordinates[0])
make_test_images(2, type_coordinates[1])
make_test_images(3, type_coordinates[2])
