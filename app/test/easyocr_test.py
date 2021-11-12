import cv2
import os
import easyocr


#test_image_path = "saliency/result"
#test_image_path = "saliency"
test_image_path = "circle"
files = [(file.split('.')[0],file.split('.')[1]) for file in os.listdir(test_image_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
sorted(files)
#print(files)
for file, file_type in files:
    print(f"{file}.{file_type}", end=" : ")
    
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(f'{test_image_path}/{file}.{file_type}')
    #image1.png : [([[265, 157], [409, 157], [409, 271], [265, 271]], 'GS', 0.9909795558821826), ([[231, 261], [435, 261], [435, 373], [231, 373]], 'SYZ', 0.6518936170803954)]
    if len(result)>0:
        for location, string, conf in result:
            print(string, end=" ")
    print()
    #print(result)
