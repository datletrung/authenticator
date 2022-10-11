'''
Author: Dat Le
Date: April 24, 2021

capture screenshot and automatically scan QR code
'''

import cv2
import time
import pyautogui
import numpy as np
from pyzbar import pyzbar


class ScanQR():
    def __init__(self):
        pass
    
    def screenshot(self):
        '''
        take screenshot
        '''
        img = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img


    def scan(self, mode=0, img_path=None):
        '''
        mode:
            0 - screenshot
            1 - import image
        img_path: if 'mode' is import image: require path to the image
        '''
        if mode == 0:
            while True:
                img = self.screenshot()
                cv2.imshow('', cv2.resize(img, (img.shape[1]//3, img.shape[0]//3)))

                if cv2.waitKey(1) == ord('q'):
                    cv2.destroyAllWindows()
                    break
                
                
                img = cv2.cvtColor(img,0)
                barcode = pyzbar.decode(img)
                
                for obj in barcode:
                    obj = barcode[0]
                    barcodeData = obj.data.decode("utf-8")
                    barcodeType = obj.type
                    string = 'Data: ' + str(barcodeData)
                    print(string)
                #time.sleep(.2)
            return None

s = ScanQR().scan(0)




















