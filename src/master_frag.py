import sys
import os
import cryptographics
# DEBUG modules
import time


# create and append a SHA256 HMAC for authentication
def HMAC(secret_key, seqID):
    cat_input = bytes((secret_key + str(seqID)).encode('utf-8'))
    hmac = cryptographics.SHA256(cat_input)

    return hmac.encode('utf-8')

def pword_to_key(pword):
    phash = cryptographics.SHA256(bytes(pword.encode('utf-8')))
    key = phash[-16:]
    return key

# encrypt a piece
def encrypt_piece(piece, secret_key):
    crypt = cryptographics.AESCipher(secret_key)
    cipher_piece = crypt.encrypt(piece)

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
    frag_size = int((total_size - (total_size % n)) / n)
    pieces = []

    pieces.append(bytes(file_bytes[0:frag_size]))
    i=0
    for i in range(1,n-1):
        pieces.append(bytes(file_bytes[frag_size*i:(frag_size*(i+1))]))
    pieces.append(bytes(file_bytes[frag_size*(i+1):]))

    return pieces

# target file into binary string
def read_in_file(path_to_orig_file):
    with open(path_to_orig_file, 'rb') as f:
        file_bytes = f.read()
    f.close()

    return file_bytes

# write fragments to destination directory
def output_n_cleanup(fragments, old_fp, output_dir):
    for frag in fragments:
        fpath = output_dir + cryptographics.generate_key(8) + '.frg'
        with open(fpath, 'wb') as f:
            f.write(frag)
        f.close()
    try:
        os.remove(old_fp)
    except:
        print("Unable to delete: {}".format(old_fp))

# master function for fragmentation
def partition_file(argv):
    # arguments
    if_path = argv[1]
    n = int(argv[2])
    #secret_key = cryptographics.generate_key(16)
    secret_key = pword_to_key(argv[3])
    output_dir = argv[4]
    # read in file
    file_bytes = read_in_file(if_path)
    # fragment
    file_pieces = subdivide_file(file_bytes, n)
    # reassemble test
    fragments = prepare_pieces(file_pieces, secret_key)

    output_n_cleanup(fragments, if_path, output_dir)

    return (True, "Fragmentation successful")

# obtain hmac value for each fragment
def authenticate_fragments(fragments):
    hmac_dict = {}
    for frag in fragments:
        payload = frag[:-64]
        hmac = frag[-64:]
        hmac_dict[hmac] = payload

    return hmac_dict

# main function for reassembly
def reassemble(argv):
    # arguments
    
    if_path = argv[1]
    secret_key = pword_to_key(argv[2])
    success_fpath = argv[3]

    fragments = []
    frag_names = [x for x in os.listdir(if_path) if '.frg' in str(x)]
    if len(frag_names) == 0:
        return (False, "No fragments found at location")
    for name in frag_names:
        with open(if_path + name, 'rb') as f:
            read_fragment = f.read()
        f.close()
        fragments.append(read_fragment)
    hmac_dict = authenticate_fragments(fragments)

    retrieved_pieces = []
    
    i = 0
    while HMAC(secret_key, i) in hmac_dict:
        next_frag = HMAC(secret_key, i)
        if next_frag in hmac_dict:
            aes_cipher = cryptographics.AESCipher(secret_key)
            try:
                retrieved_pieces.append(aes_cipher.decrypt(hmac_dict[next_frag]))
            except:
                print("Decryption failed. Aborting.")
                return (False, "Decryption failed.")
        else:
            print("Authentication failed. Aborting")
            return (False, "Authentication failed.")
        i+=1
    reassembled_file = b''.join(retrieved_pieces)

    with open(success_fpath + "/reassembled_file.txt", 'wb') as f:
        f.write(reassembled_file)
    f.close()

    # delete used fragments
    for old_frag in frag_names:
        try:
            os.remove(if_path + old_frag)
        except:
            print("Unable to delete: {}".format(if_path + old_frag))
            return (True, "Unable to delete fragments after reassembly")

    return (True, "Assembly successful")


def validate_arguments(argv):
    # check for correct commandline arguments before advancing to demo logic
    if len(argv) != 2 and len(argv) != 3:
        print("Incorrect number of arguments. Format:")
        print("<path_to_file_to_frag> <number_of_fragments>")
        exit()
    elif len(argv) == 2:
        output = reassemble(argv)
    elif len(argv) == 3:
        try:
            int(argv[2])
        except ValueError:
            print("Incorrect type of arguments. Format:")
            print("<(string) path_to_file_to_frag> <(int) number_of_fragments>")
        output = partition_file(argv)
    if output[0]:
        print(output[1])


if __name__ == "__main__":
    validate_arguments(sys.argv)