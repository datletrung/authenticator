# Authenticator
Sick of checking your phone everytime you are asked for the 2FA code?
An Authenticator App for PC that can:
  - import by scanning QR Code directly on screen or from picture,
  - import and export secret key to transfer between devices,
  - automatically enter the 2FA Code to website.
  
## Prerequisites
  opencv-python, pyotp, qrcode, pyautogui, pillow, pyzbar, cryptography

## Installing
  - Download or clone the project
  - Install the prerequisites packages
  - Run Authenticator.py

## Running
  - On the first run, the app will ask you to set an app password. This will be use to unlock the app later
  - To add a new account, scan the QR Code of the 2FA key by 2 ways:
    * Scan directly using screen capture
    * Import from an image
  - The secret key can be manually imported to add new account to the app as well.
  - The secret key can be exported to transfer to other devices.
  - (Under developement) You can also add the URL of the 2FA website to the app and whenever you are asked for 2FA code, the app will automatically enter the code into the website.

## To do
  - Add HOPT authentication
  - QR Code capture pops up errors if the code is invalid, but keep capturing the screen and pop up even more errors
  - Integrate into Chrome Extension to catch URL and automatically enter 2FA Code

## Demo
![image](https://user-images.githubusercontent.com/39230783/195117552-1f47ce5a-886a-4c71-b2b2-272c989f7a4b.png)

## Authors  

* **Brian Le** - **Lê Trung Tất Đạt** - (https://github.com/datletrung)  
