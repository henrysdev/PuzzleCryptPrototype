import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import random
import string

# credit for pycrypto example
# https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256/12525165#12525165

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * bytes([(BS - len(s) % BS)])
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self, key ):
        if len(key) != BS:
            key = pad(key)
        self.key = key

    def encrypt( self, raw ):
        raw = pad( raw )
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

def SHA256( input_data ):
    return hashlib.sha256(input_data).hexdigest()

def generate_key( size=16 ):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))