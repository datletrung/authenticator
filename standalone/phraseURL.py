from urllib.parse import unquote


url = 'otpauth://totp/datletrung0922?secret=OV5SZ6NIV55HKOPS6QUHLJUQVVS5FJ2Q&digits=6&issuer=Facebook'
url = 'otpauth://totp/letrung@gmail.com?secret=OV5SZ6NIV55ASWPS6ADWLJHFCVS5FJ2Q&digits=6&issuer=Google'
#url = 'otpauth://totp/df?secret=OV5SZ6NIV55ASWPS6ADWLJHFCVS5FJ2Q'
#url = 'otpauth://totp/letrung@gmail.com?digits=6&issuer=Google'

key_type = unquote(url[url.find('://')+3:url.find('/', url.find('://')+3)])
username = unquote(url[url.find('/', url.find('://')+4)+1:url.find('?', url.find('/')+1)])
info = url[url.find('?', url.find('/')+1)+1:].split('&')

secret_key = ''
issuer = ''

for i in info:
    if 'secret' in i:
        secret_key = unquote(i.replace('secret=', ''))
    elif 'issuer' in i:
        issuer = unquote(i.replace('issuer=', ''))

if not secret_key:
    account_name = None
    print('Invalid URL')
elif issuer and not username:
    account_name = issuer
elif not issuer and username:
    account_name = username
elif issuer and username:
    account_name = issuer + ' (' + username + ')'

print(key_type)
print(username)
print(info)
print(secret_key, issuer)
print(account_name)
