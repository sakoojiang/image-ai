import cv2
import time,os
import skimage.io as io
import base64


def image2HtmlTag(imgPath):
    with open(imgPath, "rb") as f:
        img_data = f.read()
    img_base64 = base64.b64encode(img_data).decode()
    img_html = f'<img src="data:image/png;base64,{img_base64}">'
    return img_html



def  imageOutput(img):
    current_timestamp = int(time.time())
    tmpFile = str(current_timestamp)+".png"
    cv2.imwrite(tmpFile,img)
    retImg = io.imread(tmpFile)
    os.remove(tmpFile)
    return retImg