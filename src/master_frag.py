import sys

def read_in_file(path_to_orig_file, n):
    with open(path_to_orig_file, 'r+b') as f:
        read_data = f.read()
    f.close()
    total_size = len(read_data)
    frag_size = (total_size - (total_size % n)) / n
    pieces = []
    pieces.append(b'')
    i = 0 # iterator position in string
    p = 1 # current piece
    while i < len(read_data):
        pieces[p-1] += read_data[i:(i+1)]
        if p < n and i >= frag_size * p:
            pieces.append(b'')
            p+=1
        i+=1
    for piece in pieces:
        print(piece)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Incorrect number of arguments. Format:")
        print("<path_to_file_to_frag> <number_of_fragments>")
        exit()
    path = sys.argv[1]
    frag_count = int(sys.argv[2])
    read_in_file(path, frag_count)