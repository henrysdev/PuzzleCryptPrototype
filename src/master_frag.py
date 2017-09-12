import sys
import cryptographics

# test reassembly
def reassemble_frags(ordered_frags):
    reassembly_bytes = b''
    for frag in ordered_frags:
        print(len(frag))
        reassembly_bytes += frag
    return reassembly_bytes


def HMAC(ciphered_piece, seqID, secret_key):
    hmac = cryptographics.SHA256(bytes(secret_key + seqID))
    ciph_n_hash = ciphered_piece + hmac
    return ciph_n_hash


def encrypt_piece(piece, secret_key):
    crypt = cryptographics.AESCipher(secret_key)
    cipher_piece = crypt.encrypt(piece)
    return cipher_piece


def prepare_pieces(pieces, secret_key):
    secured_pieces = []
    for i in range(0, len(pieces)):
        ciphered = encrypt_piece(pieces[i], secret_key)
        ciph_n_hash = HMAC(ciphered_piece, secret_key)
        secured_pieces.append(ciph_n_hash)
    return secured_pieces

# split byte array into n equal-sized pieces
def fragment_file(file_bytes, n):
    total_size = len(file_bytes)
    frag_size = (total_size - (total_size % n)) / n
    pieces = []
    pieces.append(b'')

    i = 0 # iterator position in string
    p = 1 # current piece
    while i < len(file_bytes):
        if p < n and i >= frag_size * p:
            pieces.append(file_bytes[i:(i+1)])
            p+=1
        else:
            pieces[p-1] += file_bytes[i:(i+1)]
        i+=1

    return pieces

# target file into binary string
def read_in_file(path_to_orig_file):
    with open(path_to_orig_file, 'r+b') as f:
        file_bytes = f.read()
    f.close()
    return file_bytes

# main controller loop
def demo(argv):
    # arguments
    path = argv[1]
    n = int(argv[2])
    # read in file
    file_bytes = read_in_file(path)
    # fragment 
    pieces = fragment_file(file_bytes, n)
    # reassemble test
    secure_pieces = prepare_pieces(pieces)

def validate_arguments(argv):
    # check for correct commandline arguments before advancing to demo logic
    if len(argv) != 3:
        print("Incorrect number of arguments. Format:")
        print("<path_to_file_to_frag> <number_of_fragments>")
        exit()
    elif len(argv) == 3:
        try:
            int(argv[2])
        except ValueError:
            print("Incorrect type of arguments. Format:")
            print("<(string) path_to_file_to_frag> <(int) number_of_fragments>")
    demo(argv)

if __name__ == "__main__":
    validate_arguments(sys.argv)
    