import base64
from Crypto.Cipher import AES
from Crypto import Random
import json

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self ):
        # self.key = key.encode()
        self.key = "N$@n0.S3cret#1F8".encode()


    def encrypt( self, raw ):
        raw = pad(raw).encode()
        cipher = AES.new( self.key, AES.MODE_ECB )
        return base64.b64encode( cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt( enc ))
        
# enct = AESCipher()
# en_mess = enct.encrypt(json.dumps({'code': '01', 'msg':'Could not connect to server'}))
# print(en_mess)

# de_mess = enct.decrypt(en_mess)
# print(de_mess)