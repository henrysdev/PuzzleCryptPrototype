import sys
import os
import cryptographics


# create and append a SHA256 HMAC for authentication
def HMAC(secret_key, seqID):
    cat_input = bytes((secret_key + str(seqID)).encode('utf-8'))
    hmac = cryptographics.SHA256(cat_input)
    return hmac.encode('utf-8')


# encrypt a piece
def encrypt_piece(piece, secret_key):
    crypt = cryptographics.AESCipher(secret_key)
    cipher_piece = crypt.encrypt(str(piece))

    return cipher_piece


# prepare pieces to be distributed via encryption and HMAC
def prepare_pieces(pieces, secret_key):
    secured_pieces = []
    for i in range(0, len(pieces)):
        cipher_piece = encrypt_piece(pieces[i], secret_key)
        ciph_n_hash = cipher_piece + HMAC(secret_key, i)
        secured_pieces.append(ciph_n_hash)

    return secured_pieces


# split byte array into n equal-sized pieces
def subdivide_file(file_bytes, n):
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
    with open(path_to_orig_file, 'rb') as f:
        file_bytes = f.read()
    # must delete file after splitting
    f.close()

    return file_bytes


def output_fragments(fragments):
    for frag in fragments:
        fpath = 'OUT_FOLDER/' + cryptographics.generate_key(8)
        with open(fpath, 'wb') as f:
            f.write(frag)
        f.close()

# main controller loop
def partition_file(argv):
    # arguments
    path = argv[1]
    n = int(argv[2])
    secret_key = cryptographics.generate_key(16)
    print("SECRET KEY: {}".format(secret_key))
    # read in file
    file_bytes = read_in_file(path)
    # fragment
    file_pieces = subdivide_file(file_bytes, n)
    # reassemble test
    fragments = prepare_pieces(file_pieces, secret_key)

    for piece in fragments:
        print('\n{}'.format(piece))

    output_fragments(fragments)


def authenticate_fragments(fragments):
    hmac_dict = {}
    for frag in fragments:
        payload = frag[:-64]
        hmac = frag[-64:]
        hmac_dict[hmac] = payload

    return hmac_dict


def reassemble(argv):
    secret_key = "1PPKT5BPMA3LVB4M" #DEBUG KEY
    # argument handling
    success_fpath = argv[1]
    fragments = []
    if_path = "OUT_FOLDER/"
    frag_names = os.listdir(if_path)
    for name in frag_names:
        with open(if_path + name, 'rb') as f:
            read_fragment = f.read()
        f.close()
        fragments.append(read_fragment)
    hmac_dict = authenticate_fragments(fragments)
    print(hmac_dict)

    retrieved_pieces = []
    #retrieved_file = b''
    n = len(fragments)
    for i in range(0,n):
        next_frag = HMAC(secret_key, i)
        if next_frag in hmac_dict:
            aes_cipher = cryptographics.AESCipher(secret_key)
            try:
                retrieved_pieces.append(aes_cipher.decrypt(hmac_dict[next_frag]))
                #retrieved_file += aes_cipher.decrypt(hmac_dict[next_frag])
            except:
                print("Decryption failed. Aborting.")
                exit()
        else:
            print("Authentication failed. Aborting")
    reassembled_file = b''.join(retrieved_pieces)
    #reassembled_file = retrieved_file

    print("successful")

    with open("RASM_FOLDER/reassembled_file.txt", 'wb') as f:
        f.write(reassembled_file)
    f.close()


def validate_arguments(argv):
    # check for correct commandline arguments before advancing to demo logic
    if len(argv) != 2 and len(argv) != 3:
        print("Incorrect number of arguments. Format:")
        print("<path_to_file_to_frag> <number_of_fragments>")
        exit()
    elif len(argv) == 2:
        reassemble(argv)
    elif len(argv) == 3:
        try:
            int(argv[2])
        except ValueError:
            print("Incorrect type of arguments. Format:")
            print("<(string) path_to_file_to_frag> <(int) number_of_fragments>")
        partition_file(argv)


if __name__ == "__main__":
    validate_arguments(sys.argv)
    