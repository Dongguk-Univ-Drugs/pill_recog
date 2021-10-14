from darknet import darknet_images

if __name__ == '__main__':
    results = darknet_images.test()
    print(results)