import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self, key ):
        if len(key) != BS:
            print("incorrect key length... padding for you")
            key = pad(key)
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

class SHA256:
    def __init__( self, input_data ):
        self.input_data = input_data
        return hashlib.sha256(base64.b64encode(self.input_data)).hexdigest()
        
"""
mycipher = AESCipher("passcode")
encr_msg = mycipher.encrypt("MY MESSAGE")
print(encr_msg)
decr_msg = mycipher.decrypt(encr_msg)
print(decr_msg)
hashed_str = hashlib.sha256("my passcode".encode('utf-8')).hexdigest()
print(hashed_str)
"""