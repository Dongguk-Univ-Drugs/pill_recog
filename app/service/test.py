# import cv2
# from preprocessing import Preprocessing

# pp = Preprocessing()

# img_path = '../test/cuba.png'

# img = cv2.imread(img_path)
# # img = pp.remove_noise(img)
# gray = pp.get_grayscale(img)
# # dilated = pp.dilate(gray)
# # cannyed = pp.canny(dilated)
# thres = pp.thresholding(gray)

# cv2.imshow("test", thres)
# cv2.waitKey(0)
"""test easyocr"""
import easyocr
import argparse
import cv2


def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True)
ap.add_argument('-l', '--langs', type=str, default='en')
ap.add_argument('-g', '--gpu', type=int, default=-1)
args = vars(ap.parse_args())

langs = args['langs'].split(',')

image = cv2.imread(args['image'])

reader = easyocr.Reader(langs, gpu=args['gpu'] > 0)
results = reader.readtext(image)

for bbox, text, prob in results:
    print('INFO: {:.4f}:{}'.format(prob, text))

    tl, tr, br, bl = bbox
    tl = (int(tl[0]), int(tl[1]))
    tr = (int(tr[0]), int(tr[1]))
    br = (int(br[0]), int(br[1]))
    bl = (int(bl[0]), int(bl[1]))

    text = cleanup_text(text)

    cv2.rectangle(image, tl, br, (0, 255, 0), 3)
    cv2.putText(image, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 255, 0), 2)

cv2.imshow('image', image)
cv2.waitKey(0)