import hashlib
import platform

info = platform.machine() +'|'+ platform.system() +'|'+ platform.processor()
print(info)

hashed = hashlib.sha512(info.encode()).hexdigest()
arr = []
for i in range(0, len(hashed)-1, 32):
    if i+32 <= len(hashed):
        arr.append(hashed[i:i+32])
arr = arr[::-1]
arr = ''.join(arr)

hashed = hashlib.md5(arr.encode()).hexdigest()[:32]

print(hashed)
