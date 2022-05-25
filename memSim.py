from audioop import add
from cgi import print_arguments
import sys

PAGE_SIZE = 256
TLB_SIZE = 16

class StatTracker:
    def __init__(self):
        self.num_trans_addrs = 0
        self.page_faults = 0
        self.page_attempts = 0
        self.tlb_hits = 0
        self.tlb_misses = 0
        
    def getTLBHitRate():
        return 3
    
    def getTLBHits(self):
        return self.tlb_hits
    
    def incTLBHits(self):
        self.tlb_hits += 1
        
    def getTLBMisses(self):
        return self.tlb_misses
    
    def incTLBMisses(self):
        self.tlb_misses += 1
        
    def getPageFaults(self):
        return self.page_faults
    
    def incPageFaults(self):
        self.page_faults += 1
    
    def getNumTransAddresses(self):
        return self.num_trans_addrs
    
    def incNumTransAddresses(self):
        self.num_trans_addrs += 1
        
    # def printSummary():
    #     print(F"{address}, {rbyteInteger},")
    #     print(F"Number of Translated Addresses = 10")
    #     print(F"Page Faults = 10")
    #     print(F"Page Fault Rate = 1.000")
    #     print(F"TLB Hits = 0")
    #     print(F"TLB Misses = 10")
    #     print(F"TLB Hit Rate = {getTLBHitRate()}")


class PhysicalMemory:
    def __init__(self, nf):
        self.memory = [None] * nf
        self.num_frames = nf
        self.length = 0
    
    def setFrame(self, frame_num, data):
        self.memory[frame_num] = data
    
    def getNumFrames(self):
        return self.num_frames
        
    def isFull(self):
        return None not in self.memory
            
    def getLength(self):
        return self.length
    
    def setLength(self, num):
        self.length = num
        
    # def getAvailableFrameNum(self):
    #     return self.length

             
class TLB:
    def __init__(self):
        self.tlb = {}

    def addEntry(self, page, frame):
        if len(self.tlb.keys()) == TLB_SIZE:
            self.tlb.pop(list(d.keys()).pop(0))
        self.tlb.update({page : frame})  
            
    def is_empty(self):
        return len(self.tlb.keys()) == 0
    
    def findPage(self, page):
        return page in self.tlb.keys()
    
    def getFrame(self, page):
        return self.tlb[page]

class PageTable:
    def __init__(self):
        self.pt = {}

    def updateEntry(self, page, frame, v_bit):
        self.pt.update({tuple((page, frame)): v_bit})      
    
    def findEntry(self, page, frame):
        return (page, frame) in self.pt.keys()
    
    def getValidBit(self, page, frame):
        return self.pt.get(tuple((page, frame)))     
      
def printHeader(address):
    page_num = address // PAGE_SIZE
    offset = address % PAGE_SIZE
    referenced_byte = accessBackingStore(PAGE_SIZE * page_num + offset, 1)
    rbyteInteger = int.from_bytes(referenced_byte, 'little', signed=True)
    print(F"{address}, {rbyteInteger},")
    
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
  
  
# Ask Tessa if a Cache Miss is if the Page and the Frame don't match up.
# def getAvailableIndex(mem, lru_tracker):
#     if(mem.isFull()):
        
#     else:
#         mem.getLength()
        
    
    
    # lru_index = lru_tracker.pop()
    # lru_tracker.insert(0,lru_index)
#     return lru_index

def LRU(vAddresses, tlb, pt, mem, stats):
    # mem = [None] * num_frames
    lru_tracker = [range(0,mem.getNumFrames())]
    
    for vAddress in vAddresses:
        # open_index = getAvailableIndex(mem, lru_tracker)
        processAddressLRU(vAddress, tlb, pt, mem, lru_tracker)
        printHeader(vAddress)
        
        # print(accessBackingStore(PAGE_SIZE * i, 1)) when you find the frame, spit out contents

def updateLRUTracker(lru_tracker, tlb):
    lru_frame = lru_tracker.remove(tlb.getFrame())
    lru_tracker.insert(0,lru_frame)

def processAddressLRU(vAddress,  tlb, pt, mem, lru_tracker, stats):
    page = vAddress // PAGE_SIZE
    offset = vAddress % PAGE_SIZE
    
    if(tlb.findPage(page)):
        updateLRUTracker(lru_tracker, tlb)
        stats.incTLBHits()
        return   
    elif(tlb.findEntry()):
        return
    
# def FIFO(vAddresses, frames):
#     return

# def OPT(vAddresses, frames):
#     return

def main(argv):
    FRAMES = 256
    PRA = "FIFO"
    stats = StatTracker()
    tlb = TLB() 
    page_table = PageTable()
    vAddresses = getVirtualAddresses(argv[0])
        
    for i in range(1, len(argv)):
        if argv[i].isnumeric():
            FRAMES = int(argv[i])
        elif argv[i] == "LRU" or argv == "OPT":
            PRA = argv[i]
            
    mem = PhysicalMemory(FRAMES)
            
    if PRA == "FIFO":
        FIFO(vAddresses, tlb, page_table, mem, stats)
    elif PRA == "OPT":
        OPT(vAddresses, tlb, page_table, mem, stats)
    else:
        LRU(vAddresses, tlb, page_table, mem, stats)

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
