from urllib import request

images_url = {}
with open('drug_images_100.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        id, url = line.split('\t')
        images_url[id] = url
#print(images_url)
for id, url in images_url.items():
    print(url)
    image = request.urlopen(url).read()
    save_image = open(f'origin_images/{id}.png', 'wb')
    save_image.write(image)
    save_image.close()

