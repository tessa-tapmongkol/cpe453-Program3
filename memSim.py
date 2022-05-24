import sys


# backing_store.seek(p * PAGE_SIZE + d, 0)
# ref_byte = backing_store.read(1)
# ref_byte_int = int.from_bytes(ref_byte, 'little', signed=True)
# https://www.geeksforgeeks.org/python-seek-function/ 


PAGE_SIZE = 256
TLB_SIZE = 16
TLB = []
PageTable = []
# backingStore = []

def main(argv):
    FRAMES = 256
    PRA = "FIFO"

    # backingStore = readBackingStoreFile("BACKING_STORE.bin")
    vAddresses = getVirtualAddresses(argv[0])
    print(vAddresses)
    
    for i in range(1, len(argv)):
        if argv[i].isnumeric():
            FRAMES = int(argv[i])
        elif argv[i] == "LRU" or argv == "OPT":
            PRA = argv[i]
            
    if PRA == "FIFO":
        FIFO(vAddresses, FRAMES)
    elif PRA == "OPT":
        OPT(vAddresses, FRAMES)
    else:
        LRU(vAddresses, FRAMES)
        
# def readBackingStoreFile(filename):
#     b_store = []
#     file = open(filename,"rb")
#     bytes = file.read(256).hex()
#     while bytes:
#         b_store.append(bytes) 
#         print(bytes)
#         bytes = file.read(256).hex()
#     file.close()
#     return b_store

# Given a byte offset and number of bytes to read,
# opens Backing Store, moves file descriptor to offset
# and reads the number of bytes from the offset
def accessBackingStore(offset, num_of_bytes):
    file = open("BACKING_STORE.bin","rb")
    file.seek(offset, 0)
    bytes_read = file.read(num_of_bytes)
    file.close()
    return bytes_read

# Gets virtual addresses from user specified text file
def getVirtualAddresses(filename):
    vAddresses = []
    file = open(filename, "r")
    lines = file.readlines()
    for line in lines:
        vAddresses.append(int(line))
    file.close()
    return vAddresses

def FIFO(vAddresses, frames):
    return

def OPT(vAddresses, frames):
    return

def LRU(vAddresses, frames):
    return

class TLB_Entry:
    def __init__(self, page, frame):
        self.page = page
        self.frame = frame

class PageTable_Entry:
    def __init__(self, page, frame, valid):
        self.page = page
        self.frame = frame
        self.valid = valid

if __name__ == "__main__":
    main(sys.argv[1:])
    # main(sys.argv)
