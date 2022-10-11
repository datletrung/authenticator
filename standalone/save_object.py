import os
import time
import pyotp
import base64
import pickle
import hashlib
import platform
from cryptography.fernet import Fernet

class StoreData():
    def __init__(self):
        info = platform.machine() +'|'+ platform.system() +'|'+ platform.processor() +'|XOyxcU6QZHKexzpi4orOlxRua8rytbSy'
        hashed = hashlib.sha512(info.encode()).hexdigest()
        hashed = ' '.join([hashed[i:i+32] for i in range(0, len(hashed), 32)])
        hashed = hashed[::-1]
        hashed = ''.join(hashed)


        key = hashlib.md5(hashed.encode()).hexdigest()[:32]
        key = base64.urlsafe_b64encode(key.encode())
        self.fernet = Fernet(key)

    def save(self, arr, filename):
        try:
            obj = pickle.dumps(arr, pickle.HIGHEST_PROTOCOL)
            encrypted = self.fernet.encrypt(obj)
            with open(filename, 'wb+') as f:
                f.write('DO NOT DELETE OR MODIFY THIS FILE!\n'.encode())
                f.write(encrypted)
            return True
        except:
            print('Cannot save data to', filename)
            return False
            

    def load(self, filename):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, 'rb') as f:
                encrypted_reload = f.readlines()[1]
                decrypted = self.fernet.decrypt(encrypted_reload)
            arr = pickle.loads(decrypted)
            return arr
        except Exception as e:
            print('Cannot load data from', filename)
            return False



s = StoreData()
filename = 'secret_key.dat'


arr = s.load(filename)

print(arr)

