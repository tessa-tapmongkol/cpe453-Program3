from audioop import add
from cgi import print_arguments
import sys


# backing_store.seek(p * PAGE_SIZE + d, 0)
# ref_byte = backing_store.read(1)
# ref_byte_int = int.from_bytes(ref_byte, 'little', signed=True)
# https://www.geeksforgeeks.org/python-seek-function/ 


PAGE_SIZE = 256
TLB_SIZE = 16
Tlb = [None] * TLB_SIZE
PageTable = []

# The full address (from the reference file)
# The value of the byte referenced (1 signed integer)
# The physical memory frame number (one positive integer)
# The content of the entire frame (256 bytes in hex ASCII characters, no spaces in between)
# new line character
def printHeader(address):
    page_num = address // PAGE_SIZE
    offset = address % PAGE_SIZE
    referenced_byte = accessBackingStore(PAGE_SIZE * page_num + offset, 1)
    rbyteInteger = int.from_bytes(referenced_byte, 'little', signed=True)
    print(F"{address}, {rbyteInteger},")
    
class TLB:
    def __init__(self):
        self.tlb = []

    # We can get rid of TLB and keep python tuples?? This way allows us to keep them
    def add_entry(self, page, frame):
        self.tlb.append(tuple((page, frame)))
        if len(self.tlb) == 17:
            self.tlb.pop(0)
    
    def findEntry(self, page, frame):
        return (page, frame) in self.tlb
            
# class TLB_Entry:
#     def __init__(self, page, frame):
#         self.page = page
#         self.frame = frame

class PageTable_Entry:
    def __init__(self, page, frame, valid):
        self.page = page
        self.frame = frame
        self.valid = valid

def comp_tlb_entries(tlb_e1, tlb_e2):
    return tlb_e1.page ==  tlb_e1.page and tlb_e1.frame == tlb_e1.frame

def main(argv):
    tlb = TLB() 
    FRAMES = 256
    PRA = "FIFO"
    vAddresses = getVirtualAddresses(argv[0])
    
    for i in range(1, len(argv)):
        if argv[i].isnumeric():
            FRAMES = int(argv[i])
        elif argv[i] == "LRU" or argv == "OPT":
            PRA = argv[i]
            
    if PRA == "FIFO":
        FIFO(vAddresses, FRAMES, tlb)
    elif PRA == "OPT":
        OPT(vAddresses, FRAMES, tlb)
    else:
        LRU(vAddresses, FRAMES, tlb)
        
def LRU(vAddresses, num_frames):
    for vAddress in vAddresses:
        LRU_Helper(vAddress, num_frames)
        printHeader(vAddress)
        
        # print(accessBackingStore(PAGE_SIZE * i, 1)) when you find the frame, spit out contents

    # print(accessBackingStore(0, 256))


# Total number of page faults and a % page fault rate
# Total number of TLB hits, misses and % TLB hit rate
def LRU_Helper(vAddress, num_frames):
    # TLB 
    # PageTable
    return 3
    
    

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

if __name__ == "__main__":
    main(sys.argv[1:])    
        
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
