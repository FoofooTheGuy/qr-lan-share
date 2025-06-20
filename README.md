# qr-lan-share
Download files over LAN by scanning a QR code

# About
This was created as a simpler alternative to [3dsend](https://github.com/MeatReed/3dsend). It is intended to be used with the remote install feature of [FBI](https://github.com/TheRealZora/FBI-Reloaded) to install .cia files directly from a URL

# Usage
![image](https://github.com/user-attachments/assets/24d7f114-4f12-4806-a289-6c32c9ad7499)

## Install dependencies
1. Install [python](https://www.python.org/downloads/) to run this script.
2. Install [qrcode](https://pypi.org/project/qrcode/)
3. Install [pillow](https://pypi.org/project/pillow/)
4. Install [tkinterdnd2](https://pypi.org/project/tkinterdnd2/)

## Navigating the GUI
1. Click on "Browse" to choose a file, or drag and drop a file onto the button to select that file.
2. Change the port or keep it default if you do not care.
3. Click on "Start Server" to generate the QR code and start the http server

## Quirks
Beware that this will copy the entire .cia file to a temporary directory, QRLS_temp/tmp.cia, essentially doubling the space that the file takes up on the drive until the directory is removed. This is done to reduce the size of the QR code.
