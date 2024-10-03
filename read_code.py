#https://qiita.com/igor-bond16/items/0dbef691a71c2e5e37d7
#https://qiita.com/PoodleMaster/items/0afbce4be7e442e75be6
from pyzbar.pyzbar import decode
import cv2

def readCode (frame):
    barcodeData = ''
    x = y = w = h = 0

    font = cv2.FONT_HERSHEY_SIMPLEX
    d = decode (frame)
    if d:
        for barcode in d:
            x, y, w, h = barcode.rect
            barcodeData = barcode.data.decode ('utf-8')
            print (barcodeData, x, y, w, h)

    return barcodeData, x, y, w, h

# #img = cv2.imread('barcode_arcode.jpg')
# #img = cv2.imread('barcode.png')
# img = cv2.imread('qrcode.png')
# d = decode (img)
# if d:
#     for barcode in d:
#         x, y, w, h = barcode.rect
#         barcodeData = barcode.data.decode ('utf-8')
#         print (barcodeData, x, y, w, h)

# cap = cv2.VideoCapture (0, cv2.CAP_DSHOW)
# font = cv2.FONT_HERSHEY_SIMPLEX

# while cap.isOpened ():
#     ret, frame = cap.read ()
#     if ret == True:
#         barcodeData, x, y, w, h = readCode (frame)
#         cv2.rectangle (frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
#         frame = cv2.putText (frame, barcodeData, (x, y-10), font, .5, (0, 0, 255), 2, cv2.LINE_AA)
#         cv2.imshow('frame', frame)

#     if cv2.waitKey (1) & 0xFF == ord ('q') :
#         break

# cap. release () 