import time
import pyotp

#otpauth://totp/datletrung0922?secret=OV5SZ6NIV55HKOPS6QUHLJUQVVS5FJ2Q&digits=6&issuer=Facebook
#OV5SZ6NIV55HKOPS6QUHLJUQVVS5FJ2Q
#totp = pyotp.TOTP('OV5SZ6NIV55HKOPS6QUHLJUQVVS5FJ2Q')
totp_1 = pyotp.TOTP('OV5SZ6NIV55HKOPS6QUHLJUQVVS5FJ2Q')
totp_2 = pyotp.TOTP('OV5SZ6NIV55HKOPS6QUHLJUQVVS5FJ2Q'.lower())

while True:
    print(totp_1.now() + '|' + totp_2.now())
    time.sleep(1)
    
